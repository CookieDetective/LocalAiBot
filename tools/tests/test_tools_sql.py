import os
import sqlite3
import pytest

from tools.sql import list_tables, run_sqlite_query

DB_PATH = "db.sqlite"

@pytest.fixture(scope="module")
def use_existing_db():
    # Do NOT remove or recreate the db file.
    # Just ensure it exists for the test.
    assert os.path.isfile(DB_PATH), "db.sqlite does not exist in the project root."
    yield

def test_list_tables(use_existing_db):
    tables = list_tables()
    print(tables)
    assert "users" in tables

def test_run_sqlite_query_count(use_existing_db):
    result = run_sqlite_query("SELECT COUNT(*) FROM Users;")
    assert isinstance(result, list)
    assert result[0][0] == 2000