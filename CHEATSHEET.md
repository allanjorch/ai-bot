AI Telegram Bot - Cheat Sheet
STARTING & STOPPING
| Action                     | Command                                      |
|----------------------------|----------------------------------------------|
| Start the stack            | docker-compose up -d                         |
| Stop the stack             | docker-compose down                          |
| Restart bot only           | docker-compose restart bot                   |
| Restart Ollama only        | docker-compose restart ollama                |
| Full restart               | docker-compose down && docker-compose up -d  |
---
WATCHING LOGS
| Action                     | Command                                      |
|----------------------------|----------------------------------------------|
| Watch bot logs             | docker-compose logs -f bot                   |
| Watch Ollama logs          | docker-compose logs -f ollama                |
| Watch all logs             | docker-compose logs -f                       |
| Last 50 lines (bot)        | `docker-compose logs bot | tail -50`         |
---
CHANGING MODELS
Pull a new model
docker exec ollama ollama pull <model-name>
Switch to a downloaded model
# 1. Edit .env
# 2. Change: OLLAMA_MODEL=<model-name>
# 3. Restart: docker-compose restart bot
Example workflow
# Pull qwen3:4b
docker exec ollama ollama pull qwen3:4b
# Switch to it
# Edit .env → OLLAMA_MODEL=qwen3:4b
docker-compose restart bot
Check downloaded models
docker exec ollama ollama list
---
MAKING CHANGES TO bot.py
# 1. Edit bot.py with your changes
# 2. Rebuild and restart
docker-compose up -d --build
---
CONFIGURATION FILES
| File               | Purpose                                      |
|--------------------|----------------------------------------------|
| .env               | Tokens and model settings                    |
| docker-compose.yml | Container orchestration                      |
| bot.py             | Bot logic and behavior                       |
| Dockerfile         | Bot container build instructions             |
| requirements.txt   | Python dependencies                          |
---
ENVIRONMENT VARIABLES (.env)
TELEGRAM_TOKEN="your_token"
OLLAMA_MODEL=qwen3:8b
To switch models, only change OLLAMA_MODEL:
OLLAMA_MODEL=phi3:mini
# OR
OLLAMA_MODEL=mistral:7b
# OR
OLLAMA_MODEL=qwen3:4b
---
TROUBLESHOOTING
| Problem                     | Solution                                      |
|-----------------------------|-----------------------------------------------|
| Bot not responding          | docker-compose logs -f bot                    |
| Can't reach Ollama          | docker-compose logs ollama                    |
| Model not found             | docker exec ollama ollama pull <model>        |
| Something feels wrong       | docker-compose down && docker-compose up -d   |
---
QUICK REFERENCE COMMANDS
# Status check
docker-compose ps
# List downloaded models
docker exec ollama ollama list
# Pull a new model
docker exec ollama ollama pull <name>
# View current model in use
docker-compose logs bot | grep "Starting with model"
# Stop everything
docker-compose down
---
MODELS TESTED ON YOUR HARDWARE
| Model      | Size   | Speed   | Quality    |
|------------|--------|---------|------------|
| phi3:mini  | ~3 GB  | ⚡ Fast | Good       |
| qwen3:4b   | ~2.5 GB| ⚡ Fast | Better     |
| mistral:7b | ~4 GB  | Medium  | Very Good  |
| qwen3:8b   | ~5.2 GB| Slow    | Excellent  |
---
SECURITY NOTES
- Token stored in .env (gitignored)         ✓
- Containers are isolated                   ✓
- All processing happens locally            ✓
- Token regenerated? Update .env + restart
