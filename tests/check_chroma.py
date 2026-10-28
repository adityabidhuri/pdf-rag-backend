
from vector_store import collection

document_id = 3
owner_id = 2

results = collection.get(
    where={
        "$and": [
            {"document_id": document_id},
            {"owner_id": owner_id},
        ]
    },
    include=["metadatas"],
)

print("Total chunks in ChromaDB:", collection.count())
print("Chunks for this document:", len(results["ids"]))
print("Chunk IDs:", results["ids"])
print("Chunk metadata:", results["metadatas"])
