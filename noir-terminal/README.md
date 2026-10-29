# 👻 NoirTerminal: Ghost in the Machine

> *A haunted terminal companion built for the Hacktoberfest 2026 Open-Source AI Challenge: Week 4 ("Ghost in the Machine").*

NoirTerminal acts as a spooky wrapper proxy for your shell. It executes your real terminal commands safely, preserves their output completely intact inside hardcoded cryptographic borders, and uses local open-source AI to weave file-aware horror, custom ASCII art, and creepy atmospheric commentary around your results.

---

## **Prerequisites**

Make sure you have the following installed and set up on your machine:
1. **Python 3.14+**
2. **[uv](https://github.com/astral-sh/uv)** (Fast Python package and script runner)
3. **LM Studio** (Running a local open-weight model, e.g., `qwen2.5-3b-instruct`, with the local server started on port `1234`)

---

## **Configuration (`config.json`)**

You can customize your local model and API settings without touching the script code by editing `config.json`:

```json
{
  "api_url": "http://localhost:1234/v1/chat/completions",
  "model": "qwen2.5-3b-instruct",
  "temperature": 0.95,
  "max_tokens": 400
}