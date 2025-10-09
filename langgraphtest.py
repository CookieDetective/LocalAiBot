from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

def read_json(filename: str) -> dict:
    """Read a JSON file and return its contents."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def read_excel(filename: str, sheet_name: str = None) -> dict:
    """
    Read an Excel file and return its contents as a dictionary.
    If sheet_name is None, reads the first sheet.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(filename, sheet_name=sheet_name)
        # If multiple sheets, df will be a dict of DataFrames
        if isinstance(df, dict):
            # Convert all dataframes to dict
            return {name: sheet.to_dict(orient="records") for name, sheet in df.items()}
        else:
            # Single sheet, convert to dict
            return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

agent = create_react_agent(
    model="gpt-3.5-turbo",
    tools=[read_json, read_excel],
    prompt="You are a helpful assistant"
)

# Run the agent
#result = agent.invoke(
#    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
#)
result = agent.invoke(
    {"messages": [{"role": "user", "content": "read the incidents from private/incTestData.xlsx and tell me about the third INC"}]}
)
#result = read_json("private/contacts.json")
# If result['messages'] is a list of objects with 'content' and maybe 'role' or 'type':
for msg in reversed(result['messages']):
    # If using LangChain/Graph, AIMessage may have a 'content' and possibly 'additional_kwargs'
    if hasattr(msg, "content") or ("content" in msg if isinstance(msg, dict) else False):
        # Optionally check if msg is an AIMessage
        if getattr(msg, "role", None) == "assistant" or getattr(msg, "type", None) == "ai" or "AIMessage" in str(type(msg)):
            print(msg.content if hasattr(msg, "content") else msg["content"])
            break
        # If your structure doesn't have role, just print the last item with content
        elif "content" in msg:
            print(msg["content"])
            break