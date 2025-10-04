from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM
from langchain.chains import ConversationChain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
from tools.sql import list_tables
from app.persona.persona import Persona
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from tools.web_search import web_search

def build_chat(persona=None):
    persona = persona or Persona()
    # Build the memory (simple, in-memory for now)
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

    # Set up the LLM (Ollama)
    #llm = OllamaLLM(model="mixtral:8x7b")
    llm = ChatOllama(model="llama3.1:8b",
                     temperature=0).bind_tools([web_search])

    messages = [
        SystemMessagePromptTemplate.from_template(
            "You are a helpful AI assistant. You have access to the tool 'web_search', which can search the web if needed."
        ),
        HumanMessagePromptTemplate.from_template(
            "{input}"
        )
    ]

    prompt = ChatPromptTemplate(
        input_variables=["input"],
        messages=messages
    )

    # Build the chain for conversational chat
    #conversation = ConversationChain(
    #    llm=llm,
    #    memory=memory,
    #    prompt=prompt
    #)
    chain = prompt | llm
    return chain
    #return conversation

if __name__ == "__main__":
    chain = build_chat()
    chain.invoke({
        "input": "I love programming."
    })