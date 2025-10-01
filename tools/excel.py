import os
import pandas as pd
from pydantic import BaseModel

class ReadExcelArgsSchema(BaseModel):
    file_path: str
    sheet_name: str | None = None

class SummarizeExcelArgsSchema(BaseModel):
    file_path: str
    sheet_name: str | None = None

class FindRowArgsSchema(BaseModel):
    file_path: str
    sheet_name: str | None = None
    column: str
    value: str

def read_excel(file_path: str, sheet_name: str = None):
    """Reads an Excel file and returns the first few rows as a 2D array (list of lists).
    The first row contains column names.
    If reading all sheets, returns a dict: {sheet_name: 2D array}
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # If reading all sheets, df will be a dict
        if isinstance(df, dict):
            result = {}
            for sheet, sheet_df in df.items():
                # Get first few rows as 2D array (including column names)
                rows = [list(sheet_df.columns)] + sheet_df.head().values.tolist()
                result[sheet] = rows
            return result
        else:
            # Single sheet: Get first few rows as 2D array (including column names)
            return [list(df.columns)] + df.head().values.tolist()
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"

def summarize_excel(file_path: str, sheet_name: str = None):
    """Summarizes an Excel sheet by returning column names and the number of rows."""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # If all sheets are read, df is a dict of DataFrames
        if isinstance(df, dict):
            result = []
            for sheet, sheet_df in df.items():
                summary = f"Sheet: {sheet}\nColumns: {', '.join(sheet_df.columns)}\nTotal rows: {len(sheet_df)}"
                result.append(summary)
            return "\n\n".join(result)
        else:
            summary = f"Columns: {', '.join(df.columns)}\nTotal rows: {len(df)}"
            return summary
    except Exception as e:
        return f"Error summarizing Excel file: {str(e)}"

def find_row_in_excel(file_path: str, sheet_name: str = None, column: str = "", value: str = ""):
    """Finds the first row in the Excel sheet where column matches value.
    If sheet_name is None, searches all sheets and returns the first match.
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # If reading all sheets, df is a dict of DataFrames
        if isinstance(df, dict):
            # Search each sheet for a matching row
            for sheet, sheet_df in df.items():
                if column not in sheet_df.columns:
                    continue
                matches = sheet_df[sheet_df[column] == value]
                if not matches.empty:
                    return f"Sheet: {sheet}\nFirst matching row:\n{matches.head(1).to_string(index=False)}"
            return f"No rows found with {column} = {value} in any sheet."
        else:
            if column not in df.columns:
                return f"Column '{column}' not found in sheet."
            matches = df[df[column] == value]
            if matches.empty:
                return f"No rows found with {column} = {value}."
            return f"First matching row:\n{matches.head(1).to_string(index=False)}"
    except Exception as e:
        return f"Error finding row in Excel file: {str(e)}"

from langchain.tools import Tool

read_excel_tool = Tool(
    name="read_excel",
    func=read_excel,
    description="Read and preview the first few rows of an Excel file. Arguments: file_path, sheet_name (optional).",
    args_schema=ReadExcelArgsSchema
)

summarize_excel_tool = Tool(
    name="summarize_excel",
    func=summarize_excel,
    description="Summarize the columns and number of rows in an Excel sheet. Arguments: file_path, sheet_name (optional).",
    args_schema=SummarizeExcelArgsSchema
)

find_row_tool = Tool(
    name="find_row_in_excel",
    func=find_row_in_excel,
    description="Find the first row in an Excel sheet where a column matches a given value. Arguments: file_path, sheet_name (optional), column, value.",
    args_schema=FindRowArgsSchema
)