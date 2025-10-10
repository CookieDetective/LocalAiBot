import json
import pandas as pd

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