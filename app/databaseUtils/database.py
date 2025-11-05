"""
databaseUtils/database.py

Builds a vector store from Document objects and exposes a retriever tool,
following the pattern in tutorials/db_tutorial.py.

This module:
- builds an in-memory vector store using InMemoryVectorStore (from the tutorial)
- wraps the retriever into a LangChain tool via create_retriever_tool
- exposes helper functions for building and querying

Notes:
- InMemoryVectorStore is ephemeral; swap in a persistent store (Chroma, FAISS on disk, Milvus, etc.)
  for production usage.
- By default this uses OpenAIEmbeddings() as in the tutorial; you can pass a different embedding
  implementor (sentence-transformers wrapper, HuggingFaceEmbeddings, etc.)
"""

from __future__ import annotations

import os
import logging
import sys
from typing import Tuple

from dotenv import load_dotenv

# langchain-style components used in the tutorial
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_classic.tools.retriever import create_retriever_tool

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def build_vectorstore_from_documents(documents, embedding=None) -> Tuple[object, object]:
    """
    Build a vector store from a list of langchain Document objects.

    Args:
        documents: list of Document objects (e.g., output of split_documents)
        embedding: an embedding instance (e.g., OpenAIEmbeddings() or other). If None,
                   an OpenAIEmbeddings() instance will be created (requires OPENAI_API_KEY).

    Returns:
        (vectorstore, retriever) where retriever = vectorstore.as_retriever()
    """
    if embedding is None:
        logger.info("No embedding provider passed; using OpenAIEmbeddings() by default")
        embedding = OpenAIEmbeddings()

    logger.info("Creating InMemoryVectorStore from %d documents", len(documents))
    vectorstore = InMemoryVectorStore.from_documents(documents=documents, embedding=embedding)
    retriever = vectorstore.as_retriever()
    logger.info("Built vectorstore and retriever")
    return vectorstore, retriever


def make_retriever_tool(retriever, name: str = "retrieve_documents", description: str = ""):
    """
    Wrap a retriever in a LangChain tool for use by agentic models or orchestration graphs.

    Args:
        retriever: the retriever object from vectorstore.as_retriever()
        name: tool name
        description: tool description

    Returns:
        a tool object created by create_retriever_tool(...)
    """
    if not description:
        description = "Retrieve semantically similar documents from the vector store."
    tool = create_retriever_tool(retriever, name, description)
    logger.info("Created retriever tool: %s", name)
    return tool


def retrieve_with_tool(tool, query: str, n_results: int = 3):
    """
    Convenience wrapper to invoke the retriever tool.

    Args:
        tool: the retriever tool (created with make_retriever_tool)
        query: query string
        n_results: number of results requested (tool-specific; many wrappers accept this param)

    Returns:
        The raw response from tool.invoke(...)
    """
    logger.info("Invoking retriever tool with query: %s", query)
    # Many tool wrappers expect a dict with a "query" key like the tutorial example
    return tool.invoke({"query": query, "n_results": n_results})


if __name__ == "__main__":
    """
    Basic demo: import documentProcessing to load & split web pages (tutorial URLs),
    build an in-memory vectorstore, wrap a retriever tool, and run a sample query.
    """
    logger.info("Running databaseUtils/database.py demo")

    # Attempt to import documentProcessing from the repository root.
    try:
        import documentProcessing as dp
    except Exception:
        # If running as a package or different cwd, try adding parent path
        logger.info("documentProcessing import failed; trying parent directory hack")
        parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if parent not in sys.path:
            sys.path.insert(0, parent)
        import documentProcessing as dp  # try again

    example_urls = [
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
        "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
        "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
    ]

    try:
        docs = dp.load_web_documents(example_urls)
        splits = dp.split_documents(docs, chunk_size=100, chunk_overlap=50)

        vectorstore, retriever = build_vectorstore_from_documents(splits)
        tool = make_retriever_tool(retriever, name="retrieve_blog_posts",
                                   description="Search and return information about Lilian Weng blog posts.")
        # run a test query similar to the tutorial
        res = retrieve_with_tool(tool, "types of reward hacking", n_results=3)
        print("=== Retriever tool response ===")
        print(res)
    except Exception as exc:
        logger.exception("Demo failed: %s", exc)