#!/usr/bin/env python3
# /// script
# dependencies = [
#     "requests",
# ]
# ///
"""
NoirTerminal - Haunted Terminal Proxy (Hardcoded Borders Edition)
Guarantees identical, permanent borders around real output, with fully dynamic LLM horror outside.
"""

import sys
import subprocess
import argparse
import requests
import json

LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def get_horrific_haunting(command: str, raw_output: str) -> dict:
    """Asks the LLM only for the dynamic commentary text outside the hardcoded borders."""
    system_prompt = (
        "You are a terrifying, blood-soaked digital ghost haunting a Windows terminal. "
        "Analyze the provided command and actual command output. "
        "Write horrific, chilling, file-aware short sentences mentioning specific file names found in the output, packed with scattered emojis (💀, 🩸, 👁️, 🕷️, 🕯️, 🔪, 👻). "
        "Return a JSON object with EXACTLY these 2 keys:\n"
        '- "top_haunting": A chilling commentary string to display ABOVE the real output.\n'
        '- "bottom_haunting": A terrifying sentence or observation to display BELOW the real output.\n'
        "IMPORTANT: Output ONLY valid raw JSON. No markdown blocks (no ```json), no extra commentary."
    )

    user_prompt = f"Command executed: {command}\n\nActual Command Output:\n{raw_output[:800]}"

    payload = {
        "model": "qwen2.5-3b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.95,
        "max_tokens": 300,
        "stream": False
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=payload, timeout=30)
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
    parser = argparse.ArgumentParser(description="Haunted Terminal Proxy - Hardcoded Border Edition")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="The command to execute")
    
    args = parser.parse_args()
    if not args.cmd:
        print("👻 *No command provided to haunt.*")
        sys.exit(1)
        
    full_command = " ".join(args.cmd)

    # 1. Execute command securely via PowerShell on Windows
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

    # 2. Get dynamic LLM commentary
    haunting = get_horrific_haunting(full_command, combined_output)

    # 3. Define permanent, 100% hardcoded borders
    top_border = "╔══════════════════════════════════════════════════════════╗"
    bottom_border = "╚══════════════════════════════════════════════════════════╝"

    # 4. Print everything in order
    print()
    # Dynamic LLM top commentary
    if "top_haunting" in haunting:
        print(f"\033[31m{haunting['top_haunting']}\033[0m")
    
    # Permanent Top Border
    print(f"\033[35m{top_border}\033[0m")
    
    # Pristine Real Output
    if saved_stdout:
        print(saved_stdout, end="")
    if saved_stderr:
        print(saved_stderr, file=sys.stderr, end="")

    # Permanent Bottom Border
    print(f"\033[35m{bottom_border}\033[0m")

    # Dynamic LLM bottom commentary
    if "bottom_haunting" in haunting:
        print(f"\033[31m{haunting['bottom_haunting']}\033[0m")
    print()

    sys.exit(return_code)

if __name__ == "__main__":
    main()