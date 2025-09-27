from langchain.memory import ConversationBufferMemory
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from app.persona.persona import Persona
from langchain.prompts import PromptTemplate

def build_chat(persona=None):
    persona = persona or Persona()
    # Build the memory (simple, in-memory for now)
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

    # Set up the LLM (Ollama)
    llm = Ollama(model="mixtral:8x7b")  # Change model if needed

    # Strong persona prompt template
    prompt_text = (
        "{history}\n"
        "User: {input}\n"
        f"{persona.name}:"
        "\n\n"
        f"Instructions: You are {persona.name}. {persona.description}\n"
        f"{getattr(persona, 'prompt_suffix', '')}\n"
        "Always respond in a manner consistent with your persona, using your unique style, vocabulary, and manner of speaking."
    )

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=prompt_text
    )

    # Build the chain for conversational chat
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt
    )

    return conversation, persona