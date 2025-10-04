from langchain.document_loaders import JSONLoader

class MultiJSONLoader:
    def __init__(self, file_paths, jq_schema="."):
        """
        file_paths: list of str, paths to JSON files.
        jq_schema: str, jq-style query to extract fields from JSON.
                   Default is '.' (whole document).
        """
        self.file_paths = file_paths
        self.jq_schema = jq_schema

    def load_documents(self):
        docs = []
        for path in self.file_paths:
            loader = JSONLoader(
                file_path=path,
                jq_schema=self.jq_schema,
                text_content=False
            )
            docs.extend(loader.load())
        return docs
