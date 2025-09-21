from langchain.tools import tool
import wikipedia
from persona import ArchivistPersona

persona = ArchivistPersona()

@tool
def wiki_tool(query: str) -> str:
    """Searches Wikipedia for a topic and returns a scholarly summary, saving page and sources in organized folders."""
    results = wikipedia.search(query, results=1)
    if not results:
        persona.add_note(f"Wikipedia search for '{query}' yielded no results.")
        return persona.persona_style("No Wikipedia results found for your query.")
    page_title = results[0]
    try:
        page = wikipedia.page(page_title, auto_suggest=False)
        html_path, sources_path = persona.save_wikipedia_page(query, page_title, page.html(), page.references)
        summary = wikipedia.summary(page_title, sentences=5)
        note = persona.persona_reference_note("wikipedia", query)
        return persona.persona_style(f"{summary}\n\n{note}")
    except Exception as e:
        persona.add_note(f"Error fetching Wikipedia page '{page_title}': {e}")
        return persona.persona_style(f"Error fetching Wikipedia page: {e}")