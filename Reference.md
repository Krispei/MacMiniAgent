## Running Ollama
brew services start ollama

ollama run qwen3:30b-a3b

curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:30b-a3b",
  "prompt": "Say hello",
  "stream": false
}'