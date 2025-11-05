"""
documentProcessing.py

Lightweight document processing utilities inspired by tutorials/db_tutorial.py.

This module currently:
- loads web pages using WebBaseLoader
- flattens loader output
- splits documents into smaller chunks using RecursiveCharacterTextSplitter

Planned/placeholder document types to implement (add these as TODOs or future functions):
- PDF (e.g., PyPDFLoader, UnstructuredPDFLoader)
- plain text (.txt) loader
- Microsoft Word (.docx)
- Markdown (.md) loader / directory loader
- DirectoryLoader to batch-load many files
- S3 / cloud object storage loaders
- Email/MSG loader
- OCR-based loaders for scanned documents
- Custom parsers for HTML / structured pages

Each loader's function should:
- return a list of langchain Document objects
- allow optional metadata
- be composable with split_documents(...)
"""

from __future__ import annotations

import os
import logging
from typing import List

from dotenv import load_dotenv

# langchain-style imports used in the tutorial
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Attempt to set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def load_web_documents(urls: List[str]) -> List:
    """
    Load documents from a list of URLs using WebBaseLoader.

    Returns:
        A flat list of langchain Document objects (not nested lists).
    """
    logger.info("Loading %d URLs with WebBaseLoader", len(urls))
    docs_nested = [WebBaseLoader(url).load() for url in urls]
    # flatten the list-of-lists: each loader returns a list of Document(s)
    docs = [doc for sub in docs_nested for doc in sub]
    logger.info("Loaded %d documents (after flattening)", len(docs))
    return docs


def split_documents(documents: List, chunk_size: int = 100, chunk_overlap: int = 50) -> List:
    """
    Split documents into smaller chunks suitable for embedding / indexing.

    Uses the tiktoken-backed RecursiveCharacterTextSplitter like the tutorial.

    Args:
        documents: List of langchain Document objects.
        chunk_size: token/window size for chunks (default 100 to match tutorial).
        chunk_overlap: overlap between chunks (default 50).

    Returns:
        A list of split Document objects.
    """
    logger.info(
        "Splitting %d documents into chunks (size=%d overlap=%d)",
        len(documents),
        chunk_size,
        chunk_overlap,
    )
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(documents)
    logger.info("Produced %d document chunks", len(splits))
    return splits


if __name__ == "__main__":
    """
    Basic local test when running this file directly.
 
    It loads the same example URLs used in tutorials/db_tutorial.py,
    splits them, and prints small snippets from the first few chunks.
    """
    example_urls = [
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
        "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
    ]

    try:
        docs = load_web_documents(example_urls)
        splits = split_documents(docs, chunk_size=100, chunk_overlap=50)
        # show first few chunk previews
        for i, chunk in enumerate(splits[:5]):
            content_preview = chunk.page_content.strip()[:200].replace("\n", " ")
            print(f"--- chunk {i} preview ---\n{content_preview}\n")
    except Exception as e:
        logger.exception("Error during local document processing demo: %s", e)