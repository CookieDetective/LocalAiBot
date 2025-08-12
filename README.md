# LangChain with Deepseek Coder (Ollama) - Docker on Windows

## Setup

1. **Ensure Ollama is running** on Windows and the Deepseek Coder model is pulled:
   ```
   ollama pull deepseek-coder-v2:latest
   ollama serve
   ```

2. **Clone this repo** (or create these files in your PyCharm project).

3. **Build the Docker image:**
   ```
   docker build -t langchain-ollama-example .
   ```

4. **Run the container:**  
   This will connect to Ollama on your Windows host.
   ```
   docker run -it --rm langchain-ollama-example
   ```

   - If you want to override the model or Ollama URL:
     ```
     docker run -it --rm -e OLLAMA_MODEL=deepseek-coder:33b langchain-ollama-example
     ```

## Notes

- `host.docker.internal` is the standard way for Docker containers to access services running on the Windows host.
- The container does **not** run Ollama or Deepseek; it just connects to your existing Ollama server.

## Customization

- Edit `langchain_ollama_example.py` for your LangChain workflows.
- Add dependencies to `requirements.txt` as needed.
