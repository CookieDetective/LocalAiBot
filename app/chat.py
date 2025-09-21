import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LLMChatbot:
    def __init__(self, llm_provider=None, model_name="gpt-3.5-turbo"):
        self.llm_provider = llm_provider or "openai"
        self.model_name = model_name
        self.memory = ConversationBufferMemory(return_messages=True)
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def chat(self, prompt):
        self.memory.chat_memory.add_user_message(prompt)
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for msg in self.memory.chat_memory.messages:
            role = "assistant" if msg.type == "ai" else "user"
            messages.append({"role": role, "content": msg.content})

        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            answer = response.choices[0].message.content
            self.memory.chat_memory.add_ai_message(answer)
            return answer
        else:
            raise NotImplementedError(f"Provider {self.llm_provider} not implemented yet.")