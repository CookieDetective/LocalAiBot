from app.chat import build_chat

def main():
    chat = build_chat()
    print("A.C is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = chat.invoke(user_input)
        print("A.C:", response['response'])

if __name__ == "__main__":
    main()