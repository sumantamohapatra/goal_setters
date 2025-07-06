import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

# initialize the huggingface model
model = SentenceTransformer('all-MiniLM-L6-v2')

# initialize ChromaDB
client = chromadb.PersistentClient(path="../../chroma_db")
collection = client.get_or_create_collection(name="tariff_chunks")

# load chunks.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
chunks_path = os.path.join(BASE_DIR, "data", "chunks.json")

with open(chunks_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# ingest chunks
print(f"✅ Loading {len(chunks)} chunks into ChromaDB...")

for chunk in chunks:
    content = chunk["content"]
    metadata = chunk["metadata"]
    metadata["page_number"] = chunk["page_number"]
    metadata["chunk_type"] = chunk["chunk_type"]
    chunk_id = chunk["chunk_id"]
    
    embedding = model.encode(content).tolist()
    
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[chunk_id],
        embeddings=[embedding]
    )

print(f"✅ Successfully stored {len(chunks)} chunks in ChromaDB.")
