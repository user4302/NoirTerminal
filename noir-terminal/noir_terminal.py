#!/usr/init/env python3
# /// script
# dependencies = [
#     "requests",
# ]
# ///
"""
NoirTerminal - Haunted Terminal Proxy (Strictly English Artistic Edition)
Keeps real command output safe inside a clean ASCII frame, while the LLM 
generates rich, dynamic ASCII art and English gothic Halloween flair.
"""

import sys
import subprocess
import argparse
import requests
import json

LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def get_dynamic_haunting(command: str) -> dict:
    """Asks the LLM to generate custom English ASCII art, emojis, and theatrical flair."""
    system_prompt = (
        "You are an avant-garde digital phantom haunting a computer terminal. "
        "You MUST respond ONLY in English. Do not use any other language or non-English characters. "
        "For the given command, generate a JSON object with 4 keys:\n"
        "- 'intro_art': A rich, multi-line English ASCII art piece (skulls, ghosts, bats, pumpkins, or webs) related to the command.\n"
        "- 'top_title': A dramatic, spooky English title for the top border above the real command output.\n"
        "- 'bottom_title': A dramatic English title for the bottom border below the real output.\n"
        "- 'flavor_text': A theatrical, creepy English footer warning packed with emojis (💀, 👻, 🦇, 🕯️, 🔮).\n"
        "Return ONLY valid JSON. No markdown blocks, no extra text."
    )

    payload = {
        "model": "qwen2.5-3b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Command executed: {command}"}
        ],
        "temperature": 0.9,
        "max_tokens": 400,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=payload, timeout=20)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"].strip()
            if content.startswith("```json"): content = content[7:]
            if content.startswith("```"): content = content[3:]
            if content.endswith("```"): content = content[:-3]
            return json.loads(content.strip())
    except Exception:
        pass
    
    return {
        "intro_art": "      .---.\n     /     \\\n    | () () |\n     \\  _  /\n      `-'/\n     /     \\\n    |       |\n    \\       /",
        "top_title": f"HAUNTED CRYPT ACCESS: {command}",
        "bottom_title": "VAULT SEALED",
        "flavor_text": "💀🦇 The digital veil tears open, and the spirits whisper your commands into the dark abyss... 🕯️🔮"
    }

def main():
    parser = argparse.ArgumentParser(description="Haunted Terminal Proxy")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="The command to execute")
    
    args = parser.parse_args()
    if not args.cmd:
        print("👻 *No command provided to haunt.*")
        sys.exit(1)
        
    full_command = " ".join(args.cmd)

    # 1. Execute the command securely and store output in variables
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

    # 2. Get high-creativity artistic assets from the LLM
    haunting = get_dynamic_haunting(full_command)

    # 3. Print the dynamic LLM ASCII art introduction
    print("\n\033[36m" + haunting.get("intro_art", "") + "\033[0m")

    # 4. Format borders with the dynamic LLM titles
    top_label = f" 🔮 {haunting['top_title']} "
    bottom_label = f" 👻 {haunting['bottom_title']} "
    
    box_width = max(60, len(top_label) + 4, len(bottom_label) + 4)
    
    top_border = "╔" + top_label + "═" * max(0, box_width - len(top_label)) + "╗"
    bottom_border = "╚" + bottom_label + "═" * max(0, box_width - len(bottom_label)) + "╝"

    # 5. Print protected real output inside borders
    print(f"\033[35m{top_border}\033[0m")
    
    if saved_stdout:
        print(saved_stdout, end="")
    if saved_stderr:
        print(saved_stderr, file=sys.stderr, end="")

    print(f"\033[35m{bottom_border}\033[0m")
    
    # 6. Print theatrical footer flavor text with emojis outside
    print(f"\033[33m {haunting['flavor_text']} \033[0m\n")

    sys.exit(return_code)

if __name__ == "__main__":
    main()