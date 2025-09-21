import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from langchain.tools import BaseTool
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# If modifying these SCOPES, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

NOTES_FILE = Path("google_tools/gmail_notes.txt")

class GmailBasicTool(BaseTool):
    """
    LangChain-compatible tool for basic Gmail interactions: scanning inbox, searching,
    and tracking emails the user is waiting for.
    """

    name = "gmail_basic"
    description = (
        "Tool to scan Gmail inbox, search emails by keyword/subject/sender, "
        "and track emails the user is waiting for. Requires user-provided credentials.json."
    )

    def __init__(self, credentials_path="credentials.json", token_path="token.pickle"):
        super().__init__()
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        # The token.pickle file stores the user's access and refresh tokens
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Gmail credentials file ({self.credentials_path}) not found. "
                        "Download it from Google Cloud Console and place it in the project root."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def list_recent_emails(self, max_results=10) -> List[Dict[str, Any]]:
        """
        Fetches a summary of recent emails (subject, sender, snippet, date).
        """
        results = self.service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
            headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
            snippet = msg_data.get('snippet', '')
            emails.append({
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": snippet[:200]
            })
        return emails

    def search_emails(self, query: str, max_results=5) -> List[Dict[str, Any]]:
        """
        Search emails by Gmail search query.
        Example queries: 'from:someone@example.com', 'subject:Your Invoice', 'keyword'
        """
        results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()
            headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
            snippet = msg_data.get('snippet', '')
            emails.append({
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
                "snippet": snippet[:200]
            })
        return emails

    def add_waiting_for(self, note: str):
        """
        Add a note or keyword for emails you are waiting for (e.g. 'Amazon refund', 'from:hr@company.com').
        """
        NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(note.strip() + "\n")

    def list_waiting_for(self) -> List[str]:
        """
        List all notes/keywords you are waiting for.
        """
        if not NOTES_FILE.exists():
            return []
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def check_waiting_for(self, max_results=5) -> Dict[str, List[Dict[str, Any]]]:
        """
        For each waiting-for note, search if matching emails have arrived.
        Returns a dict: {note: [matching_emails]}
        """
        results = {}
        for note in self.list_waiting_for():
            matches = self.search_emails(note, max_results=max_results)
            results[note] = matches
        return results

    def _run(self, tool_input: str) -> str:
        """
        Basic dispatcher for use with LangChain agent.
        Usage examples for tool_input:
          - "list recent"
          - "search: from:boss@example.com"
          - "track: Amazon refund"
          - "show waiting"
          - "check waiting"
        """
        tool_input = tool_input.strip().lower()
        if tool_input.startswith("list recent"):
            emails = self.list_recent_emails()
            return "\n".join(
                [f"{e['date']}: {e['from']} - {e['subject']}\n{e['snippet']}" for e in emails]
            ) or "No recent emails found."
        elif tool_input.startswith("search:"):
            query = tool_input[len("search:"):].strip()
            emails = self.search_emails(query)
            return "\n".join(
                [f"{e['date']}: {e['from']} - {e['subject']}\n{e['snippet']}" for e in emails]
            ) or f"No emails found for query: {query}"
        elif tool_input.startswith("track:"):
            note = tool_input[len("track:"):].strip()
            self.add_waiting_for(note)
            return f"Added to waiting-for list: '{note}'"
        elif tool_input.startswith("show waiting"):
            notes = self.list_waiting_for()
            return "Waiting for:\n" + "\n".join(notes) if notes else "No waiting-for notes."
        elif tool_input.startswith("check waiting"):
            results = self.check_waiting_for()
            res = []
            for note, emails in results.items():
                res.append(f"Note: {note}")
                if emails:
                    for e in emails:
                        res.append(f"  {e['date']}: {e['from']} - {e['subject']}\n    {e['snippet']}")
                else:
                    res.append("  No matching emails found.")
            return "\n".join(res)
        else:
            return (
                "Gmail Tool Usage:\n"
                "- 'list recent' to see recent emails\n"
                "- 'search: <query>' to search your inbox\n"
                "- 'track: <keyword>' to add to waiting-for\n"
                "- 'show waiting' to list waiting-for notes\n"
                "- 'check waiting' to check if emails you're waiting for have arrived"
            )

# Example for registering with LangChain agent:
# from google_tools.gmail_basic import GmailBasicTool
# gmail_tool = GmailBasicTool()
# tools = [gmail_tool, ...]