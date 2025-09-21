from langchain.tools import tool
from WikiManager import WikiManager

wiki = WikiManager()

@tool
def wiki_tool(query: str) -> str:
    """Searches Wikipedia and returns a summary of the top result."""
    results = wiki.search(query, results=1)
    if not results:
        return "No Wikipedia results found."
    page_title = results[0]
    try:
        import wikipedia
        summary = wikipedia.summary(page_title, sentences=5)
        return f"{page_title}: {summary}"
    except Exception as e:
        return f"Error fetching summary: {e}"