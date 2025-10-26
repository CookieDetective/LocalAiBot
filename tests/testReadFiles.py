# Outline tests for tools/read_files.py
# - These are intended as a starting point / skeleton for real tests.
# - Adjust imports/assertions to match the actual signatures/return types of your functions.
# - The sample_json is provided as a pytest fixture to satisfy "make the json a variable described in the testing environment".

import json
import io
import pytest
import pandas as pd
from pathlib import Path
from typing import Any
# Import the functions under test.
# Adjust the import path if your package layout differs.
from tools.read_files import read_json, read_excel, read_txt, read_file, read_file_embedding


@pytest.fixture
def sample_json():
    """
    A JSON variable available in the test environment.
    Use this if your tests need to compare against an expected JSON structure
    instead of reading from disk.
    """
    return {
        "title": "Test Document",
        "version": 1,
        "items": [
            {"id": 1, "value": "a"},
            {"id": 2, "value": "b"}
        ],
        "meta": {"author": "CookieDetective"}
    }

@pytest.fixture
def embeddings_path() -> str:
    """
    Return the path to the repository's sample_embeddings.json.

    If the file is not present in the current working directory, skip the tests
    (so CI / local runs that don't have the file won't fail).
    """
    p = Path.cwd() / "testData" /  "sample_embeddings.json"
    print('\n' + str(p))
    if not p.exists():
        pytest.skip("sample_embeddings.json not found in project root; skipping tests that expect it.")
    return str(p)


def _assert_embedding_like(e: Any):
    assert isinstance(e, list), "Expected embedding to be a list"
    assert len(e) > 0, "Expected embedding list to be non-empty"
    assert all(isinstance(v, (int, float)) for v in e), "Embedding elements must be numeric"



def test_read_json_from_filepath(tmp_path, sample_json):
    """
    Outline:
    - write sample_json to a temp file.
    - call read_json(path) and assert the returned structure matches sample_json.
    """
    p = tmp_path / "sample.json"
    p.write_text(json.dumps(sample_json), encoding="utf-8")

    result = read_json(str(p))

    # TODO: adjust assertions depending on whether read_json returns dict or string.
    assert isinstance(result, dict)
    assert result["title"] == sample_json["title"]
    assert result["meta"]["author"] == sample_json["meta"]["author"]
    assert result["items"][0]["id"] == sample_json["items"][0]["id"]


def test_read_json_from_filelike(sample_json):
    """
    Outline:
    - create an in-memory file-like object (StringIO).
    - call read_json(file_like) if your implementation supports file-like objects.
    """
    file_like = io.StringIO(json.dumps(sample_json))

    result = read_json(file_like)

    # If your read_json consumes the file-like object, it may return dict.
    assert isinstance(result, dict)
    assert result["version"] == sample_json["version"]

#Run read_json with a null variable and test that the expected error is raised
def test_read_json_null_input():
    pass

def test_read_excel_reads_expected_sheet_and_data(tmp_path):
    """
    Outline:
    - build a small pandas DataFrame and write it to an .xlsx file.
    - call read_excel(path) and assert the returned data matches.
    Notes:
    - This test uses pandas to create the file. Ensure pandas and an engine
      (like openpyxl) are available in the test environment.
    - Adjust expectations based on what read_excel returns (DataFrame, dict, list, etc.)
    """
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    excel_path = tmp_path / "sample.xlsx"
    # pandas will select an appropriate engine if available (openpyxl is common).
    df.to_excel(excel_path, index=False, sheet_name="Sheet1")

    result = read_excel(str(excel_path))

    # Example assertions assuming read_excel returns a pandas.DataFrame.
    assert hasattr(result, "columns"), "Expected a DataFrame-like result"
    assert list(result.columns) == ["col1", "col2"]
    assert int(result.loc[0, "col1"]) == 1
    assert result.loc[2, "col2"] == "c"


#Run read_json with a null variable and test that the expected error is raised
def test_read_excel_null_input():
    pass

def test_read_txt_reads_entire_file(tmp_path):
    """
    Outline:
    - write a small text file and assert read_txt returns its contents.
    - Adjust assertions if read_txt returns a list of lines instead of a full string.
    """
    content = "Line one\nLine two\nLine three"
    txt_path = tmp_path / "sample.txt"
    txt_path.write_text(content, encoding="utf-8")

    result = read_txt(str(txt_path))

    # If read_txt returns a single string:
    assert isinstance(result, (str, list))
    if isinstance(result, str):
        assert "Line two" in result
        assert result.splitlines()[0] == "Line one"
    else:
        # If it returns a list of lines:
        assert result[0] == "Line one"
        assert result[2] == "Line three"

#Run read_json with a null variable and test that the expected error is raised
def test_read_txt_null_input():
    pass


def test_actions_json_basename_matches(embeddings_path):
    """
    The embeddings JSON contains an entry for "actions.json".
    Provide a path whose basename is actions.json and expect a valid embedding.
    """
    # Provide a path (file need not actually exist)
    file_path = str(Path("some") / "dir" / "actions.json")
    emb = read_file_embedding(file_path, embeddings_path=embeddings_path)
    assert emb is not None
    _assert_embedding_like(emb)


def test_contacts_json_exact_key_matches(embeddings_path):
    """
    If the JSON contains the key "contacts.json", calling with that key should return the embedding.
    """
    emb = read_file_embedding("contacts.json", embeddings_path=embeddings_path)
    assert emb is not None
    _assert_embedding_like(emb)


def test_servicespurpose_basename_matches(embeddings_path):
    """
    The JSON contains "ServicesPurpose.txt" — requesting by that basename should return an embedding.
    """
    emb = read_file_embedding("ServicesPurpose.txt", embeddings_path=embeddings_path)
    assert emb is not None
    _assert_embedding_like(emb)


def test_servicespurpose_absolute_path_matches(embeddings_path, tmp_path):
    """
    If the function is given an absolute path whose basename matches an entry
    in the JSON, it should still return the stored embedding.
    """
    fake_file = tmp_path / "ServicesPurpose.txt"
    abs_path = str(fake_file.resolve())
    emb = read_file_embedding(abs_path, embeddings_path=embeddings_path)
    assert emb is not None
    _assert_embedding_like(emb)


def test_missing_key_returns_none(embeddings_path):
    """
    If the requested file key is not present in sample_embeddings.json, the function should return None.
    """
    emb = read_file_embedding("this_file_does_not_exist.xyz", embeddings_path=embeddings_path)
    assert emb is None

# Additional suggestions (not implemented here):
# - Add tests for error cases (missing file, malformed json, unreadable excel).
# - Parametrize tests to check multiple encodings or sheet names.
# - Mock filesystem or use monkeypatch for injected file-like behavior.