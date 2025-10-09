# LangChain with Deepseek Coder (Ollama) - Docker on Windows

## Setup

1. **Ensure dependencies are downloaded** on Windows:
   ```
   pip install -r requirements.txt
   ```

## Notes

- `host.docker.internal` is the standard way for Docker containers to access services running on the Windows host.
- The container does **not** run Ollama or Deepseek; it just connects to your existing Ollama server.

## Customization

- Edit `langchain_ollama_example.py` for your LangChain workflows.
- Add dependencies to `requirements.txt` as needed.
