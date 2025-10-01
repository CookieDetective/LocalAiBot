import json
from typing import List, Optional

class Contact:
    def __init__(self, name: str, role: str, email: str, authorized: bool, notes: str, previous_interactions: Optional[str] = None):
        self.name = name
        self.role = role
        self.email = email
        self.authorized = authorized
        self.notes = notes
        self.previous_interactions = previous_interactions

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "authorized": self.authorized,
            "notes": self.notes,
            "previous interactions": self.previous_interactions
        }

class ContactTool:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.contacts: List[Contact] = []
        self._load_contacts()

    def _load_contacts(self):
        try:
            with open(self.json_path, "r") as f:
                data = json.load(f)
                self.contacts = [
                    Contact(
                        name=c.get("name"),
                        role=c.get("role"),
                        email=c.get("email"),
                        authorized=c.get("authorized", False),
                        notes=c.get("notes", ""),
                        previous_interactions=c.get("previous interactions")
                    )
                    for c in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = []

    def save_contacts(self):
        with open(self.json_path, "w") as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=2)

    def add_contact(self, contact: Contact):
        self.contacts.append(contact)
        self.save_contacts()

    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        for contact in self.contacts:
            if contact.email == email:
                return contact
        return None

    def list_contacts(self) -> List[dict]:
        return [c.to_dict() for c in self.contacts]

    def update_contact(self, email: str, **kwargs):
        contact = self.get_contact_by_email(email)
        if contact:
            for key, value in kwargs.items():
                if hasattr(contact, key):
                    setattr(contact, key, value)
            self.save_contacts()
            return True
        return False


# Example usage:
# tool = ContactTool("contacts.json")
# tool.add_contact(Contact("Jane Doe", "Manager", "jane@example.com", True, "Main repo", None))
# print(tool.list_contacts())