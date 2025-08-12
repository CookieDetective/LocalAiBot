from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent
from tools.wiki_persona import wiki_tool
from tools.sql_persona import run_query_tool
from persona import ArchivistPersona

persona = ArchivistPersona()

model = ChatOllama(
    base_url="http://host.docker.internal:11434",
    model="mixtral:8x7b",
    streaming=False
)

prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [wiki_tool, run_query_tool]
agent = create_openai_functions_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(persona.persona_greeting())

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    try:
        result = agent_executor.invoke({"input": user_input})  # Use invoke(), not __call__
        output = result.get("output", result)
        print("\nArchivist Persona:\n")
        print(output)
        print("\n" + "="*60 + "\n")
    except Exception as e:
        persona.add_note(f"Error in chat: {e}")
        print(persona.persona_style(f"Error: {e}"))