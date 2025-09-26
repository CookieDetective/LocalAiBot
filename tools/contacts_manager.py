import json
from pathlib import Path
from typing import Optional, List, Dict
from langchain.tools import BaseTool

class ContactsManagerTool(BaseTool):
    name: str = "ContactsManager"
    description: str = (
        "Use this tool to manage contacts across platforms, "
        "list authorized/unauthorized contacts, or add new contacts."
    )

    contacts_file: str = "private/contacts.json"  # Declare as class variable

    def load_contacts(self) -> List[Dict]:
        if not self.contacts_file.exists():
            return []
        with open(self.contacts_file, "r") as f:
            return json.load(f)

    def save_contacts(self):
        with open(self.contacts_file, "w") as f:
            json.dump(self.contacts, f, indent=2)

    def is_authorized(self, instagram_handle: str) -> bool:
        for contact in self.contacts:
            if contact.get("instagram") == instagram_handle:
                return contact.get("authorized", False)
        return False

    def add_contact(self, name: str, instagram: str, authorized: bool = False, notes: str = "") -> str:
        self.contacts.append({
            "name": name,
            "instagram": instagram,
            "authorized": authorized,
            "notes": notes
        })
        self.save_contacts()
        return f"Contact '{name}' ({instagram}) added. Authorized: {authorized}"

    def list_contacts(self, authorized: Optional[bool] = None) -> List[Dict]:
        if authorized is None:
            return self.contacts
        return [c for c in self.contacts if c.get("authorized", False) == authorized]

    def _run(self, query: str) -> str:
        """
        Simple parser for natural language queries, for use as a LangChain Tool.
        Example queries:
            - "Is alice.smith authorized?"
            - "Add John Doe, john.doe, authorized"
            - "List unauthorized"
        """
        query = query.strip().lower()
        if query.startswith("is "):
            handle = query.split("is ")[1].split(" authorized")[0].replace("?", "").strip()
            return str(self.is_authorized(handle))
        if query.startswith("add "):
            try:
                _, name, instagram, auth = query.split(",", 3)
                name = name.strip()
                instagram = instagram.strip()
                authorized = "auth" in auth.strip()
                self.add_contact(name, instagram, authorized)
                return f"Added {name} ({instagram}) as {'authorized' if authorized else 'unauthorized'}."
            except Exception as e:
                return f"Failed to parse add command: {e}"
        if "list unauthorized" in query:
            return json.dumps(self.list_contacts(authorized=False), indent=2)
        if "list authorized" in query:
            return json.dumps(self.list_contacts(authorized=True), indent=2)
        if "list" in query:
            return json.dumps(self.list_contacts(), indent=2)
        return "Unknown command. Supported: is <handle> authorized?, add <name>,<handle>,<auth>, list authorized/unauthorized"

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not implemented for ContactsManagerTool.")