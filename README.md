# Copilot Tool Manager

> Enable, disable, and manage VS Code Copilot agent tools by category. Optimize your context window by selectively disabling unused tools.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

## Why This Matters

- Tool definitions consume **~22-25% of your context window**
- Disabling unused tools frees up tokens for your actual work
- Browser tools (10 tools) consume more tokens than memory tools (2 tools) combined
- No VS Code extension required — works directly with Copilot's SQLite database

## Installation

### Option 1: Git Submodule (Recommended)

```bash
cd your-project
git submodule add https://github.com/SushantGautam/copilot-tool-manager.git .github/skills/copilot-tool-manager
```

### Option 2: Manual Install

```bash
git clone https://github.com/SushantGautam/copilot-tool-manager.git
cp -r copilot-tool-manager ~/.config/Code/User/prompts/skills/
```

### Option 3: Skills Hub CLI

```bash
gh skills-hub install copilot-tool-manager
```

## Quick Start

```bash
python3 copilot-tools.py status                    # Check status
python3 copilot-tools.py disable browser           # Disable browser tools
python3 copilot-tools.py disable browser github    # Multiple categories
python3 copilot-tools.py enable browser            # Re-enable
python3 copilot-tools.py list                      # List all tools
```

## Tool Categories

| Category | Tools | Token Cost | Safe to Disable? |
|----------|-------|------------|------------------|
| **Browser** | 10 | High | ✅ Yes (unless web dev) |
| **File Operations** | 9 | Medium | ❌ No (core) |
| **Terminal** | 6 | Medium | ⚠️ Partial |
| **VS Code** | 8 | Medium | ⚠️ Partial |
| **Chat/Agents** | 3 | Low | ❌ No |
| **GitHub/Web** | 3 | Low | ✅ Optional |
| **Memory** | 2 | Low | ✅ Optional |
| **Other** | 2 | Low | ✅ Yes |

## Common Presets

### Backend/API Work
```bash
python3 copilot-tools.py disable browser github memory
```

### Web Development
```bash
python3 copilot-tools.py enable browser terminal file_ops
python3 copilot-tools.py disable memory other
```

### Minimal (Maximum Context Savings)
```bash
python3 copilot-tools.py disable browser github memory other vscode
```

## How It Works

VS Code stores tool config in SQLite:

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Code/User/globalStorage/state.vscdb` |
| Linux | `~/.config/Code/User/globalStorage/state.vscdb` |
| Windows | `%APPDATA%\Code\User\globalStorage\state.vscdb` |

The script reads/writes `chat/selectedTools` key in `ItemTable`.

## Usage as a Copilot Skill

Ask Copilot directly:
- "disable browser tools"
- "enable terminal tools"
- "show me which tools are enabled"
- "list all tools by category"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No tool config found" | Open "Configure Tools" UI first |
| Changes don't stick | Close VS Code, then run script |
| Permission denied | Check `state.vscdb` permissions |

## License

MIT © Sushant Gautam
