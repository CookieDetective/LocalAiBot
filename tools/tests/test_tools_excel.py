import os
import pandas as pd
import pytest
import openpyxl

from tools.excel import (
    read_excel,
    summarize_excel,
    find_row_in_excel
)

TEST_FILE = "incTestData.xlsx"

@pytest.fixture(scope="module")
def excel_exists():
    assert os.path.exists(TEST_FILE), f"Test file not found: {TEST_FILE}"

def test_read_excel_preview(excel_exists):
    result = read_excel(TEST_FILE)
    for item in result:
        print(item)
    assert isinstance(result,list)
    assert "Error" not in result
    # Check that some known column or value appears in the preview
    assert "Incident" in result or "OpenShift" in result



def test_summarize_excel_columns_and_rows(excel_exists):
    result = summarize_excel(TEST_FILE)
    assert isinstance(result, str)
    assert "Columns:" in result
    assert "Total rows:" in result

    # Check for the expected number of columns and their names
    expected_columns = ["Service now Opened", "Incident No.", "Description", "Posted on Teams by", "Update", "Resolution Notes"]  # <--- fill out
    for col in expected_columns:
        assert col in result, f"Column '{col}' not found in summary output"

    # Check that all columns are listed together
    columns_line = [line for line in result.splitlines() if line.startswith("Columns:")]
    assert columns_line, "No line starting with 'Columns:' found"
    actual_columns = [
        col.strip() for col in columns_line[0].replace("Columns:", "").split(",")
    ]
    assert len(actual_columns) == 6, f"Expected 6 columns, found {len(actual_columns)}"

def test_find_row_in_excel_by_value(excel_exists):
    result = find_row_in_excel(TEST_FILE, column="Incident No.", value="INC001")
    print('\n' + result)
    assert isinstance(result, str)
    assert "First matching row:" in result or "No rows found" in result or "Error" not in result

def test_find_row_in_excel_invalid_column(excel_exists):
    result = find_row_in_excel(TEST_FILE, column="NotAColumn", value="something")
    assert "Column 'NotAColumn' not found" in result

def test_find_row_in_excel_no_match(excel_exists):
    result = find_row_in_excel(TEST_FILE, column="Income", value="NotAValueAtAll")
    assert "No rows found" in result