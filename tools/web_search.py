from duckduckgo_search import DDGS
from langchain_core.tools import tool

@tool
def web_search(query, num_results=3):
    """Search the web and return a string with top results.
    args: query: String | what it is we're looking for
          num_results: int | How many results to return
    """
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append(f"- {r['title']}: {r['href']}\n  {r['body']}")
    return "\n\n".join(results)