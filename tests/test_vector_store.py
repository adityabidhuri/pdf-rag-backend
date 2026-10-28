
from vector_store import chroma_client, collection

print("ChromaDB initialized successfully")
print("Collection name:", collection.name)
print("Collection count:", collection.count())
print("Database location: ./chroma_db")
