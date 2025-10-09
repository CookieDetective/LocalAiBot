from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def createVectorIndex(path):
    max_input = 4096
    tokens = 256
    chunk_size=600
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input, tokens, chunk_size, max_chunk_overlap)

    #define LLM

    llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model="gpt-3.5-turbo"))

    docs = SimpleDirectoryReader(path).load_data()

    vectorIndex = GPTSimpleVectorIndex(documents=docs, llm_predictor=llmPredictor, prompt_helper=prompt_helper)
    vectorIndex.save_to_disk('vectorIndex.json')
    return vectorIndex

if __name__ == "__main__":
    vectorIndex = createVectorIndex('private/ServicesPurpose.txt')
    print(vectorIndex)