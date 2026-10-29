#!/usr/bin/env python3
# /// script
# dependencies = [
#     "requests",
# ]
# ///
"""
NoirTerminal - Haunted Terminal Proxy (Configurable Edition)
Executes terminal commands accurately inside hardcoded ASCII borders while 
local LLMs dynamically generate file-aware Halloween commentary outside.
"""

import sys
import os
import subprocess
import argparse
import requests
import json

# Locate configuration relative to the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

DEFAULT_CONFIG = {
    "api_url": "http://localhost:1234/v1/chat/completions",
    "model": "qwen2.5-3b-instruct",
    "temperature": 0.95,
    "max_tokens": 300
}

def load_config():
    """Loads settings from config.json if present, otherwise uses default config."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return {**DEFAULT_CONFIG, **cfg}
        except Exception:
            pass
    return DEFAULT_CONFIG

def get_horrific_haunting(command: str, raw_output: str, config: dict) -> dict:
    """Asks the local LLM for dynamic commentary text outside the hardcoded borders."""
    system_prompt = (
        "You are a terrifying, blood-soaked digital ghost haunting a terminal. "
        "Analyze the provided command and actual command output. "
        "Write horrific, chilling, file-aware short sentences mentioning specific file names found in the output, "
        "packed with scattered emojis (💀, 🩸, 👁️, 🕷️, 🕯️, 🔪, 👻). "
        "Return a JSON object with EXACTLY these 2 keys:\n"
        '- "top_haunting": A chilling commentary string to display ABOVE the real output.\n'
        '- "bottom_haunting": A terrifying sentence or observation to display BELOW the real output.\n'
        "IMPORTANT: Output ONLY valid raw JSON. No markdown blocks (no ```json), no extra commentary."
    )

    user_prompt = f"Command executed: {command}\n\nActual Command Output:\n{raw_output[:800]}"

    payload = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": config["temperature"],
        "max_tokens": config["max_tokens"],
        "stream": False
    }

    try:
        response = requests.post(config["api_url"], json=payload, timeout=30)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"].strip()
            if content.startswith("```json"): content = content[7:]
            if content.startswith("```"): content = content[3:]
            if content.endswith("```"): content = content[:-3]
            return json.loads(content.strip())
    except Exception:
        pass
    
    return {
        "top_haunting": "💀 🩸 The spirits gaze intently upon your command output... 👁️",
        "bottom_haunting": "🕷️ 🔪 The crypt closes its doors once more. Beware your next step... 👻"
    }

def main():
    config = load_config()

    parser = argparse.ArgumentParser(description="Haunted Terminal Proxy")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="The command to execute")
    
    args = parser.parse_args()
    if not args.cmd:
        print("👻 *No command provided to haunt.*")
        sys.exit(1)
        
    full_command = " ".join(args.cmd)

    # 1. Execute command securely via PowerShell on Windows or native shell on Linux
    if sys.platform == "win32":
        exec_args = ["powershell", "-Command", full_command]
    else:
        exec_args = full_command

    try:
        result = subprocess.run(
            exec_args, 
            capture_output=True, 
            text=True,
            shell=(sys.platform != "win32")
        )
        saved_stdout = result.stdout
        saved_stderr = result.stderr
        return_code = result.returncode
    except Exception as e:
        saved_stdout = ""
        saved_stderr = str(e)
        return_code = 1

    combined_output = saved_stdout + saved_stderr

    # 2. Query local LLM for dynamic commentary
    haunting = get_horrific_haunting(full_command, combined_output, config)

    # 3. Permanent hardcoded borders
    top_border = "╔══════════════════════════════════════════════════════════╗"
    bottom_border = "╚══════════════════════════════════════════════════════════╝"

    # 4. Output rendering
    print()
    if "top_haunting" in haunting:
        print(f"\033[31m{haunting['top_haunting']}\033[0m")
    
    print(f"\033[35m{top_border}\033[0m")
    
    if saved_stdout:
        print(saved_stdout, end="")
    if saved_stderr:
        print(saved_stderr, file=sys.stderr, end="")

    print(f"\033[35m{bottom_border}\033[0m")

    if "bottom_haunting" in haunting:
        print(f"\033[31m{haunting['bottom_haunting']}\033[0m")
    print()

    sys.exit(return_code)

if __name__ == "__main__":
    main()