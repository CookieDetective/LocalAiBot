from langchain.tools import tool
import sqlite3
from persona import ArchivistPersona

persona = ArchivistPersona()

@tool
def run_query_tool(query: str) -> str:
    """Run a SQL query on the local db.sqlite file and return results as text, saving query and results in organized folders."""
    db_path = "db.sqlite"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        result = "\n".join(str(row) for row in rows) if rows else "No results."
        persona.save_sql_query("database", query, result)
        note = persona.persona_reference_note("sql", "database")
        return persona.persona_style(f"Query results:\n{result}\n\n{note}")
    except Exception as e:
        persona.add_note(f"Error running query '{query}': {e}")
        return persona.persona_style(f"Error running query: {e}")