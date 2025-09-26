from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

from persona import ArchivistPersona
from tools.contacts_manager import ContactsManagerTool

def main():
    # Initialize ArchivistPersona
    persona = ArchivistPersona()
    print(persona.persona_greeting())

    # Instantiate the contacts manager as a LangChain tool
    contacts_tool = ContactsManagerTool()

    # Set up the language model (Ollama, adjust base_url/model if needed)
    model = ChatOllama(
        base_url="http://host.docker.internal:11434",
        model="mixtral:8x7b",
        streaming=False
    )

    # Prompt template: input + agent scratchpad for tool calls
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    # Create the agent with our contacts tool
    tools = [contacts_tool]
    agent = create_openai_functions_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Command-line chat loop for testing contact retrieval and editing
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        try:
            result = agent_executor.invoke({"input": user_input})
            output = result.get("output", result)
            print("\nArchivist Persona:\n")
            print(persona.persona_style(output))
            print("\n" + "="*60 + "\n")
        except Exception as e:
            persona.add_note(f"Error in chat: {e}")
            print(persona.persona_style(f"Error: {e}"))

if __name__ == "__main__":
    main()