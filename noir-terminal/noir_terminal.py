#!/usr/bin/env python3
"""
NoirTerminal - Your Spooky Terminal Commentary Bot

A lightweight shell companion that whispers creepy, noir, or ghost-story commentary
on your terminal commands using local open-weight models (Ollama/LM Studio).

Installation:
    pip install requests httpx aioshutil

Usage:
    python noir_terminal.py

Requirements:
    - Ollama installed with a small model (gemma, tinyllama, phi, etc.)
    """

import subprocess
import sys
import re
import random
from typing import Optional, Dict, List

# Sample noir/creepy commentary templates for common commands
NOIR_COMMENTARY = {
    # File operations
    "cat": [
        "👻 *The shadows reveal their secrets...* I'll read this file aloud...",
        "🎭 *Peering through the cracks of reality*... what treasures await within?",
        "💀 *A portal to hidden knowledge opens*... let's take a peek.",
    ],
    "ls": [
        "👻 *The contents materialize from nothingness*...",
        "🎭 *Let me show you what lurks in this directory*...",
        "💀 *Here they come, the digital denizens*...",
    ],
    "cd": [
        "🎭 *Ah, stepping into new territory*...",
        "👻 *The path changes... where to next?*",
        "💀 *A portal opens... welcome to the void*...",
    ],
    "rm": [
        "💀 *Don't do it!* Those files have stories... but if you must destroy them...",
        "🎭 *Erasing history, one byte at a time*...",
        "👻 *Poof! Gone forever...* Can you hear the echoes?",
    ],
    "cp": [
        "👻 *Copying memories to another place*...",
        "🎭 *Digital immortality achieved*...",
        "💀 *The same file, twice... redundancy is safety*...",
    ],
    "mv": [
        "🎭 *One more name change...* The files have new identities.",
        "👻 *Relocating data through the ether*...",
        "💀 *Moved again... never to be found*...",
    ],
    "mkdir": [
        "👻 *A new chamber is being forged in the digital realm*...",
        "🎭 *Another room opens up in this digital mansion*...",
        "💀 *Yet another folder waiting for secrets*...",
    ],
    "touch": [
        "👻 *Birth of something new...* Empty but full of potential.",
        "🎭 *An empty vessel awaits*...",
        "💀 *Created... yet unborn files, waiting to be filled*...",
    ],
    "grep": [
        "🎭 *Searching the archives for hidden truth*...",
        "👻 *The needles in digital haystacks emerge*...",
        "💀 *Patterns emerge from chaos...*",
    ],
    "find": [
        "🎭 *Calling forth lost data from the shadows*...",
        "👻 *Let's explore the dark corners of your filesystem*...",
        "💀 *Every file has a story... let me tell you theirs*...",
    ],
     "ps aux": [
        "🎭 *A parade of processes...* Each one with its own purpose.",
        "👻 *The digital workforce at work*...",
        "💀 *They keep your system alive*...",
    ],
    "top": [
        "🎭 *The digital spirits dance...* Here they are, alive and processing.",
        "👻 *A parade of processes...* Each one with its own purpose.",
        "💀 *They work while you sleep... thank you*...",
    ],
    "kill": [
        "💀 *Don't disturb them yet...* Those spirits are still at work.",
        "🎭 *Sending a message to the digital entities*...",
        "👻 *Will they hear your call?*",
    ],
    "nano": ["👻 *A simple editor, an old friend*..."],
    "vim": [
        "💀 *Vi/motion heaven awaits*...",
        "🎭 *Enter the cathedral of code...* Vim will guide you.",
    ],
    "less": [
        "🎭 *Scrolling through frozen time*...",
        "👻 *Pages from yesterday, still fresh*...",
    ],
    "more": ["👻 *An old-school page turner*..."],
    "wget": [
        "🎭 *Fetching from the digital ether*...",
        "💀 *Download complete...* The shadows now hold another file.",
    ],
    "curl": [
        "👻 *Making requests to the API spirits*...",
        "🎭 *Data flows from the void*...",
    ],
    "ssh": [
        "👻 *Opening a portal to another realm*...",
        "💀 *Who waits on that machine?*",
    ],
    "scp": ["🎭 *Copying across digital dimensions*..."],
    "git clone": [
        "👻 *Summoning code from the void*...",
        "💀 *A new repository enters existence*...",
    ],
    "git commit": [
        "🎭 *Preserving a moment in time*...",
        "👻 *History is being written*...",
    ],
    "git push": ["💀 *Sending your work to the world*..."],
    "git pull": ["👻 *Bringing down changes from above*..."],
}

# Ghost story narrative templates
GHOST_STORY_TEMPLATES = {
    "random": [
        "*The monitor flickers and whispers back at you*",
        "*You can almost hear the code typing itself*, but is it really?",
        "*A cold chill runs through your keyboard*, just as someone touches yours",
        "*Your reflection in the screen seems... different today*",
        "*The terminal cursor blinks with a rhythm only ghosts know*",
    ],
}


def get_ollama_models():
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
            servers = []
            for line in result.stdout.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 2 and 'http' in parts[0]:
                    servers.append(parts[0])
            return servers
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return []


def select_server(models: Optional[List[str]] = None, prefer_llmstudio=False) -> Optional[Dict[str, str]]:
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
        server_url = lmstudio_servers[0]
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
                available_model_names = set(model_names) & set(models)
                if available_model_names:
                    selected_model = sorted(available_model_names, key=len)[0]
                    return {
                        'type': 'lmstudio',
                        'api_url': server.rstrip('/'),
                        'model': selected_model
                    }
    
    # Fall back to Ollama
    ollama_models = models or get_ollama_models()
    
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


def make_llm_call(prompt: str, system_prompt: str, 
                  server: Dict[str, str], timeout: int = 60) -> Optional[str]:
    """Make a call to the LLM API"""
    try:
        import requests
        
        payload = {
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


def generate_commentary(command: str) -> str:
    """Generate spooky commentary for a command"""
    
    # Check if we have a specific template for this command
    base_command = re.sub(r'[|;&<>{}]', '', command).lower()
    
    if base_command in NOIR_COMMENTARY:
        commentaries = NOIR_COMMENTARY[base_command]
        commentary = random.choice(commentaries)
    else:
        # Use a general prompt for commands without templates
        prompt = f"""You are a noir detective / ghost narrator. 
        React to this terminal command with a short, spooky one-liner commentary: {command}

Respond with exactly 1 of the following formats (no explanations):
- 👻 *The shadows whisper...* [commentary]
- 🎭 *[Commentary]*
- 💀 *[Commentary]*

Example responses for reference:
- `ls`: "👻 *Here comes the digital denizens*..."
- `rm`: "💀 *Don't do it!* Those files have stories..."
- `cat`: "👻 *The shadows reveal their secrets*..."

For this command: {command}"""
        
        server = select_server()
        if server:
            commentary = make_llm_call(prompt, "", server)
            if not commentary:
                # Fallback to random template
                return random.choice(GHOST_STORY_TEMPLATES['random'])
        else:
            return random.choice(GHOST_STORY_TEMPLATES['random'])
    
    return commentary


def is_interactive_shell() -> bool:
    """Check if we're in an interactive shell"""
    try:
        result = subprocess.run(
            ['ps', '1'],
            capture_output=True,
            text=True
        )
        return 'bash' in result.stdout.lower() or 'zsh' in result.stdout.lower() or 'fish' in result.stdout.lower()
    except Exception:
        return False


def main():
    """Main entry point"""
    
    print("🎭 NoirTerminal - Your spooky terminal companion")
    print("💀 This reads commands through local LLMs (Ollama/LM Studio)")
    print()
    
    # Check if we're in an interactive shell
    if not is_interactive_shell():
        print("💀 *This script works best in an interactive shell!*")
        print("💀 Run it from your terminal session.")
        return
    
    print()
    print("👻 *Initializing... Please wait.*")
    
    # Get available models
    models = get_ollama_models()
    print(f"🎭 *Detected {len(models)} Ollama model(s): {', '.join(models[:3])}...")
    
    if not models and 'gemma' not in [m.lower() for m in ['gemma']]:
        print("💀 *No models found!* Try: ollama pull gemma:2b or ollama pull tinyllama")
    
    # Select server (default to Ollama unless specified)
    server = select_server(prefer_llmstudio=False)
    
    if not server:
        print("👻 *No LLM connection available.* Exiting.")
        return
    
    print(f"💀 *Connected to {server['type'].upper()} at {server['api_url']}")
    print()
    print("🎭 NoirTerminal is ready!")
    print()
    print("💀 *To exit: press Ctrl+C*")
    print()
    
    # Keep the process alive - monitor for new commands
    # This is a simplified version - full implementation would hook into shell events
    
    print("👻 *Listening for your commands...*")
    import time
    
    while True:
        try:
            # In a real implementation, this would wait for PROMPT_COMMAND or similar
            # For now, we'll just sleep briefly to keep the process alive
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n🎭 *Shadows fade away...*")
            break


if __name__ == "__main__":
    main()
