# 👻 NoirTerminal: Ghost in the Machine

> *A haunted terminal companion built for the Hacktoberfest 2026 Open-Source AI Challenge: Week 4 ("Ghost in the Machine").*

NoirTerminal acts as a spooky wrapper proxy for your shell. It executes your real terminal commands safely, preserves their output completely intact inside hardcoded cryptographic borders, and uses local open-source AI to weave file-aware horror, custom ASCII art, and creepy atmospheric commentary around your results.

---

## **Prerequisites**

1. **Python 3.14+**
2. **[uv](https://github.com/astral-sh/uv)** (Fast Python package manager)
3. **LM Studio** (Running a local open-weight model such as `qwen2.5-3b-instruct` on port `1234`)

---

## **Configuration (`config.json`)**

Customize your local model endpoint, model name, and inference parameters inside `config.json`:

```json
{
  "api_url": "http://localhost:1234/v1/chat/completions",
  "model": "qwen2.5-3b-instruct",
  "temperature": 0.95,
  "max_tokens": 300
}
```

---

## **🚀 Usage**

### **Direct Run**
Prefix any terminal command with `uv run`:
```bash
uv run noir_terminal.py dir
uv run noir_terminal.py git status
```

---

## **🔮 Shell Profile Integration (Auto-Haunt Commands)**

To automatically run commands through NoirTerminal without typing `uv run noir_terminal.py` every time, add an alias or wrapper function to your shell profile.

### **Windows PowerShell (`$PROFILE`)**
1. Open your profile in Notepad:
   ```powershell
   notepad $PROFILE
   ```
2. Add a helper function (replace `C:\path\to\noir-terminal` with your real path):
   ```powershell
   function haunt {
       param([Parameter(ValueFromRemainingArguments=$true)][string[]]$cmd)
       & uv run "C:\path\to\noir-terminal\noir_terminal.py" @cmd
   }
   ```
3. Save and reload:
   ```powershell
   . $PROFILE
   ```
4. Now simply run:
   ```powershell
   haunt dir
   haunt git status
   ```

### **Linux / macOS (`~/.bashrc` or `~/.zshrc`)**
1. Open your profile file:
   ```bash
   nano ~/.bashrc  # or ~/.zshrc
   ```
2. Append the wrapper function:
   ```bash
   haunt() {
       uv run /path/to/noir-terminal/noir_terminal.py "$@"
   }
   ```
3. Save and reload:
   ```bash
   source ~/.bashrc  # or source ~/.zshrc
   ```
4. Usage:
   ```bash
   haunt ls -la
   haunt git status
   ```

---

## ** Why Open Innovation Matters**
* **Total Privacy:** Your terminal command strings, repository paths, and directory contents never leave your local machine or get sent to closed cloud servers.
* **Offline Independence:** Works 100% offline with zero internet connection or third-party API keys required.