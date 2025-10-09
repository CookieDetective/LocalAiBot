from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
from tools.read_files import read_json, read_excel

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


agent = create_react_agent(
    model="gpt-3.5-turbo",
    tools=[read_json, read_excel],
    prompt="You are a helpful assistant. You can read Excel and JSON files and answer questions about their contents."
)

def get_last_assistant_message(messages):
    """Utility: returns the latest assistant message from a list of messages."""
    for msg in reversed(messages):
        if hasattr(msg, "content") and getattr(msg, "role", None) == "assistant":
            return msg.content
        elif isinstance(msg, dict) and msg.get("role") == "assistant":
            return msg["content"]
        elif hasattr(msg, "content") and "AIMessage" in str(type(msg)):
            return msg.content
        elif isinstance(msg, dict) and "content" in msg:
            return msg["content"]

if __name__ == "__main__":
    # Start a conversation with an initial message
    history = []
    print("Welcome to the Data Assistant. Ask questions about your Excel/JSON files!")

    # Optionally, start with a first message
    user_input = "read the incidents from private/incTestData.xlsx and tell me about the third INC"
    history.append({"role": "user", "content": user_input})

    while True:
        result = agent.invoke({"messages": history})
        assistant_reply = get_last_assistant_message(result['messages'])
        print(f"\nAssistant: {assistant_reply}\n")

        # Get next user input
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        history.append({"role": "user", "content": user_input})