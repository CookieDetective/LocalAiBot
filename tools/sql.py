import sqlite3
#from langchain.tools import Tool
from langchain_core.tools import tool
from pydantic.v1 import BaseModel # <Allows us to specify what kind of data we want certain classes to use
from typing import List
conn = sqlite3.connect("../db.sqlite")
@tool
def list_tables():
    """This tool returns a list of all the tables in a sqlite DB
    """
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

@tool
def run_sqlite_query(query):
    """This tool runs a sqlite query and returns the results
    args: query (String)
    """
    c = conn.cursor() #Create a cursor, an object that allows us to interact with the data base
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"
"""
#Because langchain will automatically name arguments names like '__arg1', this makes it more difficult for chatGPT to determine how to use functions
#This class will make it easier for chatGPT to understand the purpose of variables
class RunQueryArgsSchema(BaseModel):
    query: str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)
"""
@tool
def describe_tables(table_names):
    """This tool runs a sqlite query and returns the results
    args: table (String)
    """
    c = conn.cursor()
    tables = ', '.join("'"+ item + "'" for item in table_names)
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)

"""
class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema
)"""