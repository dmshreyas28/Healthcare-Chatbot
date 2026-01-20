"""
RAG Service - Handles document retrieval and embedding generation
"""
import os
from typing import List
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from config import settings


class RAGService:
    """Service for Retrieval-Augmented Generation"""
    
    def __init__(self):
        self.enabled = settings.enable_rag
        
        if not self.enabled:
            return
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=settings.vector_db_path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="healthcare_documents",
            metadata={"description": "Healthcare information documents"}
        )
    
    def add_documents(self, documents: List[str], metadata: List[dict] = None):
        """
        Add documents to the vector database
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        if not self.enabled:
            raise Exception("RAG is not enabled")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Generate IDs
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata if metadata else [{}] * len(documents),
            ids=ids
        )
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """
        Retrieve relevant context for a query
        
        Args:
            query: User's question
            top_k: Number of documents to retrieve
        
        Returns:
            Combined context from retrieved documents
        """
        if not self.enabled:
            return ""
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Combine retrieved documents
        if results and results['documents']:
            contexts = results['documents'][0]
            return "\n\n".join(contexts)
        
        return ""
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        if not self.enabled:
            return 0
        return self.collection.count()


# Global RAG service instance
rag_service = RAGService()
