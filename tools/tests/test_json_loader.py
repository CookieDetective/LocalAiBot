import unittest
import tempfile
import os
import json
from tools.json import MultiJSONLoader

class TestMultiJSONLoader(unittest.TestCase):
    def setUp(self):
        # Create temporary JSON files
        self.temp_files = []
        self.contents = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        for content in self.contents:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
            json.dump(content, tmp)
            tmp.close()
            self.temp_files.append(tmp.name)

    def tearDown(self):
        # Remove temporary files
        for file in self.temp_files:
            os.remove(file)

    def test_load_documents(self):
        loader = MultiJSONLoader(self.temp_files)
        docs = loader.load_documents()
        # Check that the loaded documents match expected content
        loaded_dicts = [doc.page_content if hasattr(doc, 'page_content') else doc for doc in docs]
        # Sometimes JSONLoader returns Document objects with page_content as stringified dicts
        # We'll convert them to dicts for comparison
        loaded_dicts = [json.loads(d) if isinstance(d, str) else d for d in loaded_dicts]
        self.assertEqual(loaded_dicts, self.contents)

if __name__ == "__main__":
    unittest.main()