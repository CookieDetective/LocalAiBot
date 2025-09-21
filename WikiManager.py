import os
import wikipedia
from pathlib import Path


class WikiManager:
    def __init__(self, base_dir="wikipedia_data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def search(self, query, results=5):
        """Search Wikipedia and return a list of page titles."""
        return wikipedia.search(query, results=results)

    def fetch_and_save_page(self, page_title, topic=None):
        """Fetch a Wikipedia page and save as HTML under a topic folder."""
        try:
            page = wikipedia.page(page_title, auto_suggest=False)
        except Exception as e:
            print(f"Error fetching page '{page_title}': {e}")
            return None

        # Use topic or the first word of the title as folder
        topic_folder = self.base_dir / (topic or page_title.split()[0])
        topic_folder.mkdir(exist_ok=True)

        # Save HTML
        html_path = topic_folder / f"{self._sanitize_filename(page_title)}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.html())

        # Save sources (references)
        sources_path = topic_folder / f"{self._sanitize_filename(page_title)}_sources.txt"
        with open(sources_path, "w", encoding="utf-8") as f:
            for ref in page.references:
                f.write(ref + "\n")

        print(f"Saved '{page_title}' to {html_path}")
        print(f"Saved sources to {sources_path}")
        return html_path

    def list_topics(self):
        """List all topic folders."""
        return [p.name for p in self.base_dir.iterdir() if p.is_dir()]

    def list_pages_in_topic(self, topic):
        """List all HTML files in a topic folder."""
        topic_folder = self.base_dir / topic
        if not topic_folder.exists():
            return []
        return [f.name for f in topic_folder.glob("*.html")]

    def _sanitize_filename(self, s):
        return "".join(c if c.isalnum() or c in " ._-" else "_" for c in s).strip()


# Example usage:
if __name__ == "__main__":
    wm = WikiManager()
    results = wm.search("LangChain", results=3)
    print("Search results:", results)
    if results:
        wm.fetch_and_save_page(results[0], topic="AI Frameworks")
        print("Topics:", wm.list_topics())
        print("Pages in 'AI Frameworks':", wm.list_pages_in_topic("AI Frameworks"))