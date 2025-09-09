from langchain.memory import ConversationBufferMemory
from langchain.llms import Ollama
from langchain.chains import ConversationChain

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