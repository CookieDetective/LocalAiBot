from app.personachat import build_chat
from app.persona.persona import Persona

def main():
    persona = Persona()

    chat, persona = build_chat(persona)

    print(f"{persona.name} is ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        print('\n')
        if user_input.lower() == "exit":
            break
        response = chat.invoke(user_input)
        print("A.C:", response['response'], '\n')

if __name__ == "__main__":
    main()