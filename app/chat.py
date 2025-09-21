from langchain.memory import ConversationBufferMemory
from langchain.llms import Ollama
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv
load_dotenv()
import openai

OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY"))

def chat_with_openai(prompt, model="gpt-3.5-turbo"):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
def build_chat():
    # Build the memory (simple, in-memory for now)
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

    # Set up the LLM (Ollama)
    llm = Ollama(model="mixtral:8x7b")  # Change model if needed

    # Build the chain for conversational chat
    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )

    return conversation