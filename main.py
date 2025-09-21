from app.chat import LLMChatbot

def main():
    print("Welcome to A.C. (modular LLM-powered chatbot)")
    print("Type 'exit' to quit.\n")

    # Initialize the modular chatbot (currently hardcoded to ChatGPT)
    chatbot = LLMChatbot()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        try:
            response = chatbot.chat(user_input)
            print(f"A.C.: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()