import logging
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmptyRetriever(BaseRetriever):
    """A retriever that always returns no documents."""
    def _get_relevant_documents(self, query: str) -> List[Document]:
        return []

class RAGSystem:
    """A system for Retrieval-Augmented Generation."""

    def __init__(self, data_path: Path, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the RAG system.

        Args:
            data_path: The path to the directory containing input documents.
            model_name: The name of the HuggingFace model for embeddings.
        """
        self.data_path = data_path
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        self.vector_store = self._create_vector_store()

    def _load_documents(self) -> list:
        """Loads all markdown documents from the data path."""
        logger.info(f"Loading documents from {self.data_path}...")
        docs = []
        for doc_path in self.data_path.glob("*.md"):
            loader = TextLoader(str(doc_path))
            docs.extend(loader.load())
        logger.info(f"Loaded {len(docs)} document(s).")
        return docs

    def _create_vector_store(self):
        """Creates a FAISS vector store from the loaded documents."""
        docs = self._load_documents()
        if not docs:
            logger.warning("No documents found to create a vector store.")
            return None

        chunks = self.text_splitter.split_documents(docs)
        if not chunks:
            logger.warning("Documents are too short to be split into chunks. RAG will work without context.")
            return None
        
        logger.info(f"Split {len(docs)} document(s) into {len(chunks)} chunks.")
        logger.info("Creating vector store...")
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        logger.info("Vector store created successfully.")
        return vector_store

    def as_retriever(self):
        """Returns the vector store as a retriever."""
        if self.vector_store is None:
            logger.warning("Vector store is not initialized. Retriever will not provide context.")
            return EmptyRetriever()
        return self.vector_store.as_retriever()
