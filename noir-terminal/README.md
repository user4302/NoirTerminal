# 🎭 NoirTerminal: Your Creepy AI Terminal Companion

A lightweight Python script that hooks into your terminal commands and uses your local open-weight model (via LM Studio or Ollama) to whisper back creepy, noir, or ghost-story commentary on the commands you run.

## Features

- ✅ Lightweight - hooks into any shell (bash, zsh, etc.)
- ✅ Local-first - runs entirely offline with local LLMs
- ✅ Custom voices - noir detective, ghost story narrator, or creepy whisper
- ✅ Low latency - minimal performance impact on your terminal

## Requirements

- Python 3.8+
- Ollama or LM Studio (with a small model like Gemma, TinyLlama, etc.)
- Any Unix/Linux/Mac shell

## Setup

1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Pull a local model:
```bash
ollama pull gemma:2b
# or try tinyllama, phi, etc.
```

3. Install dependencies:
```bash
pip install requests httpx
```

4. Run NoirTerminal:
```bash
python noir_terminal.py
```

Now replace your shell prompt with NoirTerminal and watch it whisper spooky commentary on every command you run!

## Example Output

```
$ grep -r sensitive
👻 *The shadows stretch long... let me see what secrets they hide...*
Found 42 matches in sensitive directories. A curious cat indeed.

$ cd /var/log
🎭 *Ah, the digital confessional...*
Stepping into the vault of history where mistakes are whispered in neon lights.

$ rm -rf *
💀 *Don't do it!*
Those files have stories... but if you must destroy them... go ahead, brave soul.
```

## License

MIT - use whatever spooky name you want!
