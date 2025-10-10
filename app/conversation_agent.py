from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
from tools.read_files import read_json, read_excel, read_txt
#from app.embeddings import search_embeddings
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

class ConversationAgent:
    def __init__(self):
        # Add search_embeddings to tools if ready
        self.agent = create_react_agent(
            model="gpt-3.5-turbo",
            tools=[read_json, read_excel, read_txt],  # add search_embeddings when ready
            prompt="You are a helpful assistant. You can read Excel and JSON files and answer questions about their contents."
        )
        self.history = []

    def get_last_assistant_message(self, messages):
        """Returns the latest assistant message from a list of messages."""
        for msg in reversed(messages):
            if hasattr(msg, "content") and getattr(msg, "role", None) == "assistant":
                return msg.content
            elif isinstance(msg, dict) and msg.get("role") == "assistant":
                return msg["content"]
            elif hasattr(msg, "content") and "AIMessage" in str(type(msg)):
                return msg.content
            elif isinstance(msg, dict) and "content" in msg:
                return msg["content"]

    def run(self, user_input):
        """Send user input to the agent and get the assistant's reply."""
        self.history.append({"role": "user", "content": user_input})
        result = self.agent.invoke({"messages": self.history})
        assistant_reply = self.get_last_assistant_message(result['messages'])
        self.history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply