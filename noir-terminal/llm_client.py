#!/usr/bin/env python3
"""
NoirTerminal LLM Client Module

Handles communication with Ollama and LM Studio for AI commentary generation.
"""

import subprocess
import sys
from typing import Optional, Dict, List
import requests

def get_ollama_models() -> List[str]:
    """Get list of available Ollama models"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]
            models = [line.split()[0] for line in lines if line]
            return models
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


def get_lm_studio_servers() -> List[str]:
    """Get list of running LM Studio servers"""
    try:
        result = subprocess.run(
            ["lsm", "-i"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            servers: List[str] = []
            for line in result.stdout.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 2 and 'http' in parts[0]:
                    servers.append(parts[0])
            return servers
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []

def select_server(
    models: Optional[List[str]] = None,
    prefer_llmstudio: bool = False
) -> Optional[Dict[str, str]]:
    """
    Select a server to use for the LLM.
    
    Args:
        models: List of available models (optional)
        prefer_llmstudio: Whether to prefer LM Studio over Ollama
    
    Returns:
        Dict with 'type' ('ollama' or 'lmstudio') and 'api_url', 'model'
    """
    
    # Check for running LM Studio servers first
    lmstudio_servers = get_lm_studio_servers()
    
    if prefer_llmstudio and lmstudio_servers:
        available_models = models or []
        
        if not available_models:
            print("💀 *LM Studio is running but no model is specified*...")
            print("💀 *Hint: Use ollama list to see what's available!*", file=sys.stderr)
            return None
        
        for server in lmstudio_servers:
            result = subprocess.run(
                ["curl", "-s", f"{server}/v1/models"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                import json
                models_data = json.loads(result.stdout)
                model_names = [m['name'] for m in models_data.get('models', [])]
                
                # Find common model names
                available_model_names: set[str] = set(model_names) & set(available_models)

                if available_model_names:
                    selected_model = sorted(available_model_names, key=len)[0]
                    return {
                        'type': 'lmstudio',
                        'api_url': server.rstrip('/'),
                        'model': selected_model
                    }
    
    # Fall back to Ollama
    ollama_models: List[str] = models or get_ollama_models()
    
    if ollama_models:
        model_name = ollama_models[0]
        return {
            'type': 'ollama',
            'api_url': 'http://localhost:11434/api/generate',
            'model': model_name
        }
    else:
        print("🎭 *No LLM detected!* Please install Ollama first.", file=sys.stderr)
        return None

def make_llm_call(
    prompt: str,
    system_prompt: str,
    server: Dict[str, str],
    timeout: int = 60
) -> Optional[str]:
    """Make a call to the LLM API"""
    try:
        
        payload: Dict[str, object] = {
            "model": server['model'],
            "prompt": prompt,
            "stream": False,
            "context": [],
            "temperature": 0.8,
        }
        
        response = requests.post(
            server['api_url'],
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', '')
        else:
            print(f"🎭 *API Error: {response.status_code}*")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"👻 *Connection to LLM failed: {e}*")
        return None

