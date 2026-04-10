connect to local ai

20:55:56 ~/.config/opencode $ more opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "llama.cpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LLama.cpp (local)",
      "options": {
        "baseURL": "http://192.168.2.24:30000/v1"
      },
      "models": {
        "qwen3.5-30B-A3B": {
          "name": "qwen3.5-30B-A3B"
        }
      }
    }
  }
}