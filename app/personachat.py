from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from app.persona.persona import Persona
from langchain.prompts import PromptTemplate
from app.utils.llm_selector import get_llm
from tools.sql import run_query_tool, describe_tables_tool

def build_chat(persona=None):
    persona = persona or Persona()
    # Build the memory (simple, in-memory for now)
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

    # Set up the LLM (Ollama)
    llm = get_llm()  # Change model if needed
    print(llm)

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
    tools = [run_query_tool, describe_tables_tool]

    # Build the chain for conversational chat
    #conversation = ConversationChain(
    #    llm=llm,
    #    memory=memory,
    #    prompt=prompt
    #)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
    )

    #return conversation, persona
    return agent,persona