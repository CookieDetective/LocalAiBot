from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from app.persona.persona import Persona
from tools.sql import run_sqlite_query,describe_tables  # Example: import your tool(s)
from app.utils.llm_selector import get_llm
from langchain.agents import initialize_agent, AgentType
import os

def main():
    # Choose persona as before
    persona = Persona()

    # Instantiate LLM
    llm = get_llm()
    print(llm)

    # Define prompt (customize as needed)
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are {persona.name}. {persona.description} Use tools if needed."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    # Wrap your custom tool(s)
    tools = [run_sqlite_query]  # You can add more tools here

    # Create agent and executor
    #agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # or other supported type
        verbose=True
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print(persona.intro())
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        result = agent_executor.invoke({"input": query})
        print(f"{persona.name}: {result['output']}")


if __name__ == "__main__":
    main()