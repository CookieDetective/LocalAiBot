from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent
from tools.wiki_tool import wiki_tool  # Add any other tools you want
from tools.sql import run_query_tool
from dotenv import load_dotenv
import os
load_dotenv()
ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
model = os.environ.get("OLLAMA_MODEL", "mixtral:8x22b")
#deepseek-coder-v2:latest
llm = ChatOllama(
    base_url=ollama_url,
    model=model
)


prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [wiki_tool, run_query_tool]  # Add more tools if you want

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Chat with Deepseek (with tools)! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    try:
        result = agent_executor({"input": user_input})
        # The agent_executor returns a dict with output under 'output'
        print("\nDeepseek:", result.get("output", result))
        print("\n" + "="*60 + "\n")
    except Exception as e:
        print("Error:", e)