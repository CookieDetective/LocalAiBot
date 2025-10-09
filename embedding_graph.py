import os
import json
import pickle
from typing import List, Dict, Any
from dotenv import load_dotenv

import pandas as pd
from openai import OpenAI

# Load your OpenAI API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def read_text_file(filename: str) -> str:
    """Reads a plain text file and returns its content as a string."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def read_json(filename: str) -> str:
    """Reads a JSON file and returns its content as a pretty-printed string."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error reading JSON: {e}"

def read_excel(filename: str, sheet_name: str = None) -> str:
    """
    Reads an Excel file and returns its content as a pretty-printed string.
    If sheet_name is None, reads the first sheet.
    """
    try:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if isinstance(df, dict):
            return "\n".join(
                f"Sheet: {name}\n{sheet.to_string(index=False)}"
                for name, sheet in df.items()
            )
        else:
            return df.to_string(index=False)
    except Exception as e:
        return f"Error reading Excel: {e}"

def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Gets an embedding vector for the given text using OpenAI v1+ API
    """
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def build_embeddings_for_dir(dir_path: str, embedding_model: str = "text-embedding-3-small") -> Dict[str, Any]:
    """
    Reads files and builds embeddings for each, returning {filename: embedding}
    Supports text, json, and excel files.
    """
    embeddings = {}
    for fname in os.listdir(dir_path):
        fpath = os.path.join(dir_path, fname)
        _, ext = os.path.splitext(fname)
        ext = ext.lower()
        print(f"Processing {fname}...")
        try:
            if ext in [".txt", ".md"]:
                content = read_text_file(fpath)
            elif ext == ".json":
                content = read_json(fpath)
            elif ext == ".xlsx":
                content = read_excel(fpath)
            else:
                print(f"Skipping unsupported file type: {fname}")
                continue
            print(f"Embedding {fname}...")
            embeddings[fname] = get_embedding(content, model=embedding_model)
        except Exception as e:
            print(f"Error processing {fname}: {e}")
    return embeddings

def save_embeddings_pickle(embeddings: Dict[str, Any], out_path: str):
    """Saves embeddings dict to a pickle file"""
    with open(out_path, "wb") as f:
        pickle.dump(embeddings, f)
    print(f"Saved embeddings to {out_path}")

def save_embeddings_json(embeddings: Dict[str, Any], out_path: str):
    """Saves embeddings dict to a JSON file"""
    with open(out_path, "w") as f:
        json.dump(embeddings, f)
    print(f"Saved embeddings to {out_path}")

if __name__ == "__main__":
    SAMPLE_DIR = "private"
    OUT_PATH_PICKLE = "embeddings/sample_embeddings.pkl"
    OUT_PATH_JSON = "embeddings/sample_embeddings.json"

    embeddings = build_embeddings_for_dir(SAMPLE_DIR)
    save_embeddings_pickle(embeddings, OUT_PATH_PICKLE)
    save_embeddings_json(embeddings, OUT_PATH_JSON)