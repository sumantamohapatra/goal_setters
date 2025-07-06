import os
os.environ["CHROMA_TELEMETRY"] = "FALSE"

import chromadb
from sentence_transformers import SentenceTransformer

# load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# connect to persistent ChromaDB
client = chromadb.PersistentClient(path="../../chroma_db")
collection = client.get_or_create_collection(name="tariff_chunks")

print("✅ Query interface ready. Type 'exit' to quit.")

while True:
    query = input("\nYour question: ")
    if query.lower() in ["exit", "quit"]:
        break

    query_embedding = model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3  # top 3 results
    )
    
    for i, doc in enumerate(results['documents'][0]):
        metadata = results['metadatas'][0][i]
        print(f"\nResult {i+1}:")
        print(f"Content: {doc[:500]}...")  # preview first 500 chars
        print(f"Metadata: {metadata}")
        print(f"Distance: {results['distances'][0][i]:.4f}")

print("✅ Done.")
