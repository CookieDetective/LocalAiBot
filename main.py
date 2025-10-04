from app.chat import build_chat
from app.persona.persona import Persona
from app.persona.shakespeare import ShakespearePersona

def main():
    persona_choice = input(
        "Choose persona:\n1) AI Comedian (A.C)\n2) Shakespeare\nEnter 1 or 2: "
    )
    if persona_choice == "2":
        persona = ShakespearePersona()
    else:
        persona = Persona()
    #chat, persona = build_chat(persona)
    chain = build_chat()

    print(f"{persona.name} is ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        print('\n')
        if user_input.lower() == "exit":
            break
        response = chain.invoke(user_input)
        print("A.C:", response.content.replace("\\n","\n"), '\n')

if __name__ == "__main__":
    main()