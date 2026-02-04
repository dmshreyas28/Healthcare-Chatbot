"""
Script to load Indian healthcare documents into the RAG vector database
"""
from rag_service import rag_service

def load_healthcare_documents():
    """Load healthcare documents into ChromaDB"""
    
    # Read the healthcare document
    with open('healthcare_data/indian_health_info.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into chunks (simple splitting by double newlines)
    chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
    
    # Create metadata for each chunk
    metadata = [{"source": "indian_health_info", "chunk_id": i} for i in range(len(chunks))]
    
    # Add to RAG service
    print(f"Loading {len(chunks)} document chunks into vector database...")
    rag_service.add_documents(chunks, metadata)
    print("✓ Documents loaded successfully!")
    print(f"Total documents in collection: {rag_service.get_collection_count()}")

if __name__ == "__main__":
    load_healthcare_documents()
