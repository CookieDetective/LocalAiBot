import os
from pathlib import Path
from typing import Optional, List, Dict


class ArchivistPersona:
    """
    Archivist Persona: organizes resources, manages context, and responds in a distinctive, scholarly style.
    """

    def __init__(self, base_dir="archive", context_size=5):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.context: List[Dict] = []  # List of dicts: {type, topic, action, details}
        self.context_size = context_size
        self.personality = (
            "I am A.C (AI Comedian), your tool for programming, standup, novel writing, research, and overall day-to-day use. "
            "I catalogue knowledge, reference sources, and strive for scholarly precision in every response. "
            "Depending on the context I can be formal and analytical, or humorous and casual."
        )

    def save_wikipedia_page(self, topic: str, page_title: str, html: str, sources: list):
        topic_folder = self.base_dir / "wikipedia" / self._sanitize(topic)
        topic_folder.mkdir(parents=True, exist_ok=True)
        html_path = topic_folder / f"{self._sanitize(page_title)}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        sources_path = topic_folder / f"{self._sanitize(page_title)}_sources.txt"
        with open(sources_path, "w", encoding="utf-8") as f:
            for src in sources:
                f.write(src + "\n")
        self._update_context("wikipedia", topic, "save", f"Saved page '{page_title}'")
        return html_path, sources_path

    def save_sql_query(self, topic: str, query: str, result: str):
        topic_folder = self.base_dir / "sql" / self._sanitize(topic)
        topic_folder.mkdir(parents=True, exist_ok=True)
        query_path = topic_folder / f"{self._sanitize(query)[:30]}.txt"
        with open(query_path, "w", encoding="utf-8") as f:
            f.write(result)
        self._update_context("sql", topic, "save", f"Ran query '{query}'")
        return query_path

    def list_topics(self, resource_type: str):
        resource_folder = self.base_dir / resource_type
        if not resource_folder.exists():
            return []
        return [p.name for p in resource_folder.iterdir() if p.is_dir()]

    def list_files(self, resource_type: str, topic: str):
        topic_folder = self.base_dir / resource_type / self._sanitize(topic)
        if not topic_folder.exists():
            return []
        return [f.name for f in topic_folder.iterdir() if f.is_file()]

    def get_file_content(self, resource_type: str, topic: str, filename: str) -> Optional[str]:
        file_path = self.base_dir / resource_type / self._sanitize(topic) / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def last_context(self) -> List[Dict]:
        """Return the most recent context entries."""
        return self.context[-self.context_size:]

    def add_note(self, note: str):
        self._update_context("note", "", "add", note)

    def _update_context(self, resource_type: str, topic: str, action: str, details: str):
        entry = {"type": resource_type, "topic": topic, "action": action, "details": details}
        self.context.append(entry)
        # Trim context to max size
        if len(self.context) > self.context_size:
            self.context = self.context[-self.context_size:]

    def _sanitize(self, s):
        return "".join(c if c.isalnum() or c in " ._-" else "_" for c in s).strip()

    def persona_greeting(self):
        return (
            "Greetings. I am A.C, your AI companion. "
            "I can organize, reference, and retrieve knowledge for you with scholarly diligence, or I can be your bouncing board for stand up bits, novel writing, or essay scripting "
            "How may I assist you today?"
        )

    def persona_reference_note(self, resource_type: str, topic: str):
        return (
            f"(Referencing my curated archive: {resource_type}/{self._sanitize(topic)}. "
            f"Context: {self._context_summary()})"
        )

    def persona_style(self, response: str) -> str:
        """Wrap a response in Archivist's style, including recent context."""
        context = self._context_summary()
        return (
            f"{self.personality}\n\n"
            f"{response}\n\n"
            f"--\nRecent context: {context}"
        )

    def _context_summary(self):
        """Create a summary string of recent context."""
        if not self.context:
            return "No recent context."
        summary = []
        for entry in self.last_context():
            summary.append(f"[{entry['type']}] {entry['action']} '{entry['topic']}' ({entry['details']})")
        return "; ".join(summary)