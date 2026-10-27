
from vector_store import search_chunks

question = "How much loan interest was paid?"

results = search_chunks(
    question=question,
    document_id=999999,
    owner_id=999999,
    top_k=2,
)

print("Question:", question)
print("Retrieved chunks:", len(results))

for index, chunk in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print("Source page:", chunk["page_number"])
    print("Document ID:", chunk["document_id"])
    print("Distance:", round(chunk["distance"], 4))
    print("Text:", chunk["text"])
