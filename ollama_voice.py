import os

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

import speech_recognition as sr
import pyttsx3

def say(text):
    """Speak text out loud using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the microphone and return recognized text (or empty string if failed)."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        print(f"You (voice): {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition failed: {e}")
        return ""

ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
model = os.environ.get("OLLAMA_MODEL", "deepseek-coder:2b")

llm = Ollama(
    base_url=ollama_url,
    model=model
)

print("Chat with Deepseek Coder! Say 'exit' or 'quit' to end the session.\n")
print("Press Enter to speak, or type your question and press Enter to send.")

while True:
    try:
        user_input = input("You (type, or press Enter for voice): ").strip()
        if not user_input:
            # Use microphone
            user_input = listen()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            say("Goodbye!")
            break

        prompt = PromptTemplate.from_template("{question}")
        chain = LLMChain(llm=llm, prompt=prompt)

        response = chain.invoke({"question": user_input})
        print("Deepseek:", response)
        say(str(response))
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
        say("Goodbye!")
        break