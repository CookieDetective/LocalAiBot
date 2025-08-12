from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import textwrap
from WikiManager import WikiManager  # <-- Import your WikiManager

ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
model = os.environ.get("OLLAMA_MODEL", "deepseek-coder-v2:latest")

llm = Ollama(
    base_url=ollama_url,
    model=model
)

wiki = WikiManager()

print("Chat with Deepseek Coder!")
print("Type 'exit' or 'quit' to end the session.")
print("Type 'wiki: topic' to get info from Wikipedia.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    # Wikipedia reference logic
    if user_input.lower().startswith("wiki:") or user_input.lower().startswith("reference wikipedia:"):
        query = user_input.split(":", 1)[1].strip()
        print(f"Searching Wikipedia for '{query}'...")
        results = wiki.search(query, results=1)
        if not results:
            print("No Wikipedia articles found.")
            continue
        page_title = results[0]
        html_path = wiki.fetch_and_save_page(page_title, topic=query)
        # Get a summary for the response
        try:
            import wikipedia
            summary = wikipedia.summary(page_title, sentences=5)
            prompt = PromptTemplate.from_template(
                "Using the following Wikipedia summary, answer the user's query: '{query}'.\n\nWikipedia summary:\n{summary}"
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            response = chain.invoke({"query": query, "summary": summary})
        except Exception as e:
            response = f"Error summarizing Wikipedia page: {e}"
        if isinstance(response, dict):
            response_text = response.get("text", str(response))
        else:
            response_text = str(response)
        print("\nDeepseek (Wikipedia):\n")
        print(textwrap.fill(response_text, width=100))
        print("\n" + "="*50 + "\n")
        continue

    # Normal chatbot logic
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