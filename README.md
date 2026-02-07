# AI Telegram Bot with Local LLM

A secure, private Telegram bot powered by a local large language model (Qwen3:4b).

## Overview

This project runs a Telegram bot that connects to a local Ollama instance for private, offline AI conversations. No data leaves your machine.

**Hardware:** Beelink SER8 (AMD Ryzen 7 8745HS, Radeon 780M, 64GB RAM)
**OS:** Omarchy Linux (Arch-based)

## What's Included

- **bot.py** - Telegram bot written in Python using python-telegram-bot
- **Dockerfile** - Containerized Python environment for the bot
- **docker-compose.yml** - Orchestrates Ollama + bot services
- **.env** - Environment variables (tokens, model settings)
- **.gitignore** - Excludes sensitive files

## Quick Start

```bash
# Start the stack
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## Configuration

Edit `.env` to customize:

```env
TELEGRAM_TOKEN="your_token_here"
OLLAMA_MODEL=qwen3:8b
```

To change models:
```bash
docker exec ollama ollama pull <model-name>
# Example: ollama pull gemma3:12b
```

Then update `OLLAMA_MODEL` in `.env` and restart:
```bash
docker-compose restart bot
```

## Development

When editing `bot.py`:
```bash
docker-compose up -d --build
```

## Models Tested

| Model | Size | Notes |
|-------|------|-------|
| qwen3:8b | 5.2 GB | Current - balanced, efficient |
| phi3:mini | ~3 GB | Smaller, faster but less capable |

## Security

- Token stored in `.env` (gitignored)
- Docker provides container isolation
- All processing happens locally
- No cloud dependencies

## Architecture

```
Telegram → ai-bot container → ollama container → Local LLM
                    ↓
             Docker network
```

Both services communicate via isolated Docker bridge network (`ollama-network`).

## Troubleshooting

**Bot not responding:**
```bash
docker-compose logs bot
```

**Ollama issues:**
```bash
docker-compose logs ollama
```

**Restart everything:**
```bash
docker-compose down && docker-compose up -d
```

**Check running models:**
```bash
docker exec ollama ollama list
```

## References

- Ollama: https://ollama.com
- python-telegram-bot: https://python-telegram-bot.org
- ROCm (AMD GPU): https://rocm.docs.amd.com

## License

MIT
