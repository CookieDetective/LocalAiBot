import pickle
import json
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def load_embeddings_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def load_embeddings_json(path):
    with open(path, "r") as f:
        return json.load(f)


def get_query_embedding(query, model="text-embedding-3-small"):
    response = client.embeddings.create(input=[query], model=model)
    return np.array(response.data[0].embedding)

#Replace with langgraph version sooner or later
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#currently actions.json and contacts.json
embeddings = load_embeddings_pickle("../sample_embeddings.pkl")  # or use JSON

def search_embeddings(query: str, top_n: int = 3) -> dict:
    """Return top_n most similar files to the query.
    args: query: str, top_n: int"""
    query_emb = get_query_embedding(query)
    scores = []
    for fname, emb in embeddings.items():
        score = cosine_similarity(query_emb, emb)
        scores.append((fname, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:top_n]
    return {"results": [{"filename": fname, "similarity": score} for fname, score in top]}


if __name__ == "__main__":
    # Create embeddings - type dict
    #print(embeddings)

    #Load embeddings into agent

    #Test agent ability to read embeddings

    history = []
    print("Welcome to the Data Assistant. Ask questions about your Excel/JSON files!")
