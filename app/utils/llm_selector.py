import os
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
def get_llm():
    # Read env variable (default to False if not set)
    print(os.getenv("USE_EXTERNAL_LLM"))
    use_external_llm = os.getenv("USE_EXTERNAL_LLM", "False").lower() == "true"

    if use_external_llm == True:
        # Use ChatGPT (OpenAI)
        return ChatOpenAI(model="gpt-3.5-turbo")  # Or your preferred model
    else:
        # Use Ollama local model
        return Ollama(model="mixtral:8x7b")