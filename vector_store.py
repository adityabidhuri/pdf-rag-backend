
import chromadb
from embedding_service import embed_text

# Create a persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create the collection if it doesn't already exist
collection = chroma_client.get_or_create_collection(
    name="pdf_chunks",
    metadata={"hnsw:space": "cosine"},
)



def store_chunks(chunks: list[dict],document_id: int,owner_id: int,) -> int:
    if not chunks:
        return 0

    ids = []
    texts = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        text = chunk["text"]

        embedding = embed_text(text)

        chunk_id = f"doc_{document_id}_chunk_{index}"

        ids.append(chunk_id)
        texts.append(text)
        embeddings.append(embedding)
        metadatas.append({
            "document_id": document_id,
            "owner_id": owner_id,
            "page_number": chunk["page_number"],
        })

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(ids)




def search_chunks(question: str,document_id: int,owner_id: int,top_k: int = 3,) -> list[dict]:
    if not question.strip():
        raise ValueError("Question cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    if collection.count() == 0:
        return []

    query_embedding = embed_text(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        where={
            "$and": [
                {"document_id": document_id},
                {"owner_id": owner_id},
            ]
        },
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for index, text in enumerate(results["documents"][0]):
        retrieved_chunks.append({
            "text": text,
            "page_number": results["metadatas"][0][index]["page_number"],
            "document_id": results["metadatas"][0][index]["document_id"],
            "distance": results["distances"][0][index],
        })

    return retrieved_chunks
