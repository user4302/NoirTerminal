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
import random

# Import modular components
from commands import (
    get_command_templates,
    GHOST_STORY_TEMPLATES,
)
from llm_client import select_server, make_llm_call, get_ollama_models


def generate_commentary(command: str) -> str:
    """Generate spooky commentary for a command"""
    
    try:
        # Try to get templates from NOIR_COMMENTARY dictionary
        templates = get_command_templates(command)
        commentary = random.choice(templates)
        return commentary
        
    except KeyError:
        # Command not found in templates, use LLM for dynamic generation
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