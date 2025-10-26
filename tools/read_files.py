import json
import pandas as pd
import os
from typing import List, Optional, Any

def read_json(filename: str) -> dict:
    """Read a JSON file and return its contents."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}


def read_excel(filename: str, sheet_name: str = None) -> dict:
    """
    Read an Excel file and return its contents as a dictionary.
    If sheet_name is None, reads the first sheet.
    """
    try:
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if isinstance(df, dict):
            return {name: sheet.to_dict(orient="records") for name, sheet in df.items()}
        else:
            return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

def read_txt(file_path):
    """Read and return contents of a TXT file as a string."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()



def read_file(file_path: str, sheet_name: str = None):
    """Read and return contents of files as a string."""
    if file_path.endswith(".txt"):
        return read_txt(file_path)
    elif file_path.endswith(".csv"):
        return read_excel(file_path, sheet_name=sheet_name)
    elif file_path.endswith(".json"):
        return read_json(file_path)
    else:
        raise Exception(f"Unsupported file type: {file_path}. Must be '.txt', '.csv' or '.json'.")



def read_file_embedding(
    file_path: str,
    embeddings_path: str = "sample_embeddings.json",
) -> Optional[List[float]]:
    """
    Retrieve an existing embedding for `file_path` from a JSON embeddings file.

    Important:
      - This function does NOT compute or create embeddings.
      - If an embedding exists in `embeddings_path` it is returned.
      - If no embedding is found, None is returned.
      - The function does not read the target file at `file_path`.

    Supported storage formats:
      1) Simple mapping (preferred by you):
         {
           "file1": [embedding_list],
           "file2": [embedding_list]
         }
         In this case the function will try keys in this order:
           - file_path (as provided)
           - absolute path of file_path
           - basename of file_path
      2) Document-list template (backwards-compatible with prior template):
         {
           "version": ...,
           "documents": [
             { "id": "...", "path": "/abs/path/to/file", "embedding": [...] },
             ...
           ]
         }
         In this case the function searches documents for a matching "path" or "id"
         and returns the "embedding" value.

    Args:
      file_path: path or identifier used as key when storing embeddings.
      embeddings_path: path to the JSON file containing stored embeddings.

    Returns:
      The embedding as a list of floats if found, otherwise None.
    """
    if not os.path.exists(embeddings_path):
        return None

    try:
        with open(embeddings_path, "r", encoding="utf-8") as f:
            store = json.load(f)
    except (json.JSONDecodeError, OSError):
        # If the file can't be read or parsed, behave as "not found".
        return None

    # If store is a flat mapping filename -> embedding list
    if isinstance(store, dict):
        # Quick heuristic: if all values are lists (or at least one is a list), treat as flat mapping
        # (This will also match the user's simple format.)
        has_list_values = any(isinstance(v, list) for v in store.values())
        if has_list_values and not ("documents" in store and isinstance(store.get("documents"), list)):
            # Try several key forms in order
            candidates = [
                file_path,
                os.path.abspath(file_path),
                os.path.basename(file_path),
            ]
            for key in candidates:
                if key in store and isinstance(store[key], list):
                    return store[key]
            # Not found in flat mapping
            return None

        # If store contains a "documents" list (previous template), search it
        if "documents" in store and isinstance(store["documents"], list):
            abspath = os.path.abspath(file_path)
            basename = os.path.basename(file_path)
            for doc in store["documents"]:
                if not isinstance(doc, dict):
                    continue
                # match by explicit path
                doc_path = doc.get("path")
                if doc_path and (doc_path == file_path or doc_path == abspath or os.path.basename(doc_path) == basename):
                    emb = doc.get("embedding")
                    if isinstance(emb, list):
                        return emb
                # match by id (in case user used an id key)
                if doc.get("id") in (file_path, basename):
                    emb = doc.get("embedding")
                    if isinstance(emb, list):
                        return emb

    # No embedding found
    return None