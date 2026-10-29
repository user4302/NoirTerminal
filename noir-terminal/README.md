### **🔧 Setup & Development**

---

## **Prerequisites & Installation**

This project uses:
- **Rust 1.75+** (compile-time for WASM tooling)
- **Node.js v20.x or v22.x** (runtime with pnpm)
- **[uv](https://github.com/astral-sh/uv)** (fast Python package manager - recommended first)

### **Step 1: Install uv (Recommended)**

```bash
# Windows PowerShell || Linux/macOS
winget install Astral.uv || curl -LsSf https://astral.sh/uv/install.sh | sh

# OR download binary directly
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-powershell.exe' -OutFile '$env:LOCALAPPDATA\Programs\uv.exe'" || \
curl -LO https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-linux.tar.gz && \
tar -C ~/.local/bin --strip-components=1 -xzf uv-x86_64-linux.tar.gz && rm uv-x86_64-linux.tar.gz

# Then add to PATH (Linux/macOS)
export PATH="$HOME/.local/bin:$PATH" || export PATH="/usr/local/bin:$PATH"

# Verify installation
uv --version || python -m uv --version
```

> 💡 **Why UV First?** `uv` is 10-25x faster than pip and handles dependency resolution more efficiently. It's now the recommended tool for modern Python projects.

### **Step 2: Install Python (if using uv)**

```bash
# Windows PowerShell || Linux/macOS
winget install Python.Portable.Python || sudo apt-get install python3 -y && \
curl -sSL https://bootstrap.pypa.io/get-pip.py | sudo python3 || curl -sSL https://bootstrap.pypa.io/get-pip.py | python3

# Add to PATH (Linux/macOS)
export PATH="/usr/bin/python3:$PATH" || export PATH="$HOME/.local/bin:$PATH"

# Verify Python
python --version || python3 --version
```

### **Step 3: Install Node.js (for WASM runtime)**

```bash
# Windows PowerShell || Linux/macOS
winget install OpenJS.NodeJS.LTS || sudo apt-get install nodejs -y

# Verify Node.js
node --version && npm --version
```

---

## **🚀 Quick Start**

### **Initial Setup (All Systems)**

```bash
# Windows PowerShell || Linux/macOS
cd noir-commentary/
pnpm install
```

### **Development Commands**

```bash
# Run development server
pnpm dev

# Build production version
pnpm build

# Lint and format code
pnpm lint
pnpm format

# Test suite
pnpm test

# Start Storybook
pnpm storybook
```

---

## **📝 NOIR Commentaries** (Updated Command Priority)

The `noir-commentary` system generates AI-powered comments using a multi-stage pipeline. Here are the commands with **Windows PowerShell priority** followed by **Linux equivalents**:

### **Stage 1: Code Analysis & Context Gathering**

```bash
# Windows PowerShell || Linux/macOS - Analyze codebase structure and gather context
winget install Microsoft.PowerShell || sudo apt-get install curl -y && \
curl -sSL https://api.github.com/repos/noir-project/noir/contents/contracts && \
pnpm analyze-context

# OR use the NOIR_COMMENTARY object with command alternatives
pnpm noirc --analyze || pnpm noir-analyze-context

# Windows PowerShell || Linux/macOS - Gather file dependencies and imports
winget install Microsoft.PowerShell || sudo apt-get install jq -y && \
pnpm gather-dependencies || pnpm noir-gather-deps

# Windows PowerShell || Linux/macOS - Generate type signatures from Noir code
winget install Microsoft.PowerShell || sudo apt-get install pkg-config -y && \
pnpm generate-types || pnpm noir-gen-types

### **Stage 2: AI Comment Generation**

```bash
# Windows PowerShell || Linux/macOS - Generate initial commentary (LLM)
winget install Microsoft.PowerShell || sudo apt-get install curl -y && \
curl -X POST "http://localhost:3000/api/generate-comment" \
  -H "Content-Type: application/json" \
  -d '{
    "file": "contract.noir",
    "context": "$CONTEXT$",
    "model": "claude-sonnet-4.5"
  }' | pnpm format-json || pnpm ai-generate-comment

# Windows PowerShell || Linux/macOS - Refine commentary with Noir-specific context
winget install Microsoft.PowerShell || sudo apt-get install python3 -y && \
pnpm refine-commentary || pnpm noir-refine-comments

# Windows PowerShell || Linux/macOS - Generate documentation from comments
winget install Microsoft.PowerShell || sudo apt-get install pandoc -y && \
pnpm generate-docs || pnpm noir-gen-docs

### **Stage 3: Validation & Testing**

```bash
# Windows PowerShell || Linux/macOMS - Validate Noir contracts
winget install Microsoft.PowerShell || sudo apt-get install cargo -y && \
pnpm validate-contract || pnpm noir-validate

# Windows PowerShell || Linux/macOS - Run Noir tests with commentary
winget install Microsoft.PowerShell || sudo apt-get install rustc -y && \
pnpm test-commentary || pnpm noir-test-comments

### **Stage 4: Publishing & Deployment**

```bash
# Windows PowerShell || Linux/macOS - Publish to GitHub/registry
winget install Microsoft.PowerShell || sudo apt-get install git -y && \
pnpm publish-commentaries || pnpm noir-publish

# Windows PowerShell || Linux/macOS - Deploy to CI/CD pipeline
winget install Microsoft.PowerShell || sudo apt-get install docker.io -y && \
pnpm deploy-cicd || pnpm noir-deploy
```

---

## **🔍 Troubleshooting**

### **Windows-Specific Issues**

```bash
# If uv not found on Windows
$env:PATH += ";$env:LOCALAPPDATA\Programs\uv"

# If pnpm not recognized
winget install Microsoft.PowerShell || \
sudo apt-get install curl -y && curl -fsSL https://get.pnpm.io/install.sh | sh-
```

### **Linux-Specific Issues**

```bash
# If noir-cli not found on Linux
sudo apt-get install jq python3 -y
export PATH="$HOME/.local/bin:$PATH"

# Rebuild WASM module if needed
pnpm rebuild:webassembly || pnpm wasm-rebuild
```

---

## **💡 Tips**

### **Cross-Platform Development**

1. **Use WSL on Windows**: For better Rust/Python support, consider using WSL2
2. **PowerShell vs Bash**: Commands are optimized for PowerShell first, with bash fallbacks
3. **PATH Management**: Always check `uv` and `python` paths before running commands
4. **WASM Compilation**: Build once with `pnpm build:webassembly` and cache for faster builds

### **Performance Optimization**

```bash
# Windows PowerShell || Linux/macOS - Clear TypeScript cache for faster rebuilds
winget install Microsoft.PowerShell || sudo apt-get install findutils -y && \
Remove-Item -Recurse -Force node_modules/.cache || rm -rf node_modules/.cache

# Windows PowerShell || Linux/macOS - Update pnpm store
winget install Microsoft.PowerShell || sudo apt-get install curl -y && \
pnpm store add || pnpm store update
```

---

## **📚 Contributing**

Contributions welcome! Please read our [contributing guidelines](.github/CONTRIBUTING.md) first.

### **Development Workflow**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## **🤝 Code of Conduct**

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## **💪 Security Policy**

We take security seriously. See our [security policy](.github/SECURITY.md) for details.
