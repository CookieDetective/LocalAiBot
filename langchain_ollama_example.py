from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import textwrap
from duckduckgo_search import DDGS
from tools.sql import run_query_tool

ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
model = os.environ.get("OLLAMA_MODEL", "mixtral:8x7b")

llm = Ollama(
    base_url=ollama_url,
    model=model
)

print("Chat with Deepseek Coder! Type 'exit' or 'quit' to end the session.")
print("Prefix your query with 'search:' to use the internet. (e.g., search: latest AI news)\n")

tools = [run_query_tool]

def web_search(query, num_results=3):
    """Search the web and return a string with top results."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append(f"- {r['title']}: {r['href']}\n  {r['body']}")
    return "\n\n".join(results)

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    if user_input.strip().lower().startswith("search:"):
        search_query = user_input[7:].strip()
        print("Searching the web...")
        search_results = web_search(search_query)
        # Pass results to Deepseek for summarization
        prompt = PromptTemplate.from_template(
            "Based on the following web search results, provide a helpful answer to the query: '{query}'.\n\nWeb results:\n{results}"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        try:
            summary = chain.invoke({"query": search_query, "results": search_results})
            if isinstance(summary, dict):
                summary_text = summary.get("text", str(summary))
            else:
                summary_text = str(summary)
            print("\nDeepseek (web search answer):\n")
            print(textwrap.fill(summary_text, width=100))
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print("Error:", e)
    else:
        prompt = PromptTemplate.from_template("{question}")
        chain = LLMChain(llm=llm, prompt=prompt)
        try:
            response = chain.invoke({"question": user_input})
            if isinstance(response, dict):
                response_text = response.get("text", str(response))
            else:
                response_text = str(response)
            print("\nDeepseek:\n")
            print(textwrap.fill(response_text, width=100))
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print("Error:", e)