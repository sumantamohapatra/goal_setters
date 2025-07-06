import chromadb
import os
os.environ["CHROMA_TELEMETRY"] = "FALSE"

client = chromadb.Client()
collection = client.create_collection(name="tariff_rates")

collection.add(
    documents=["Odisha residential tariff is 3.5 Rs/unit in 2024."],
    metadatas=[{"region": "Odisha", "year": 2024, "category": "residential"}],
    ids=["doc1"]
)

results = collection.query(
    query_texts=["What is the Odisha residential tariff for 2024?"],
    n_results=1
)

print(results)
