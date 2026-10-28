
from vector_store import search_chunks

question = "What information does this PDF contain?"

results = search_chunks(
    question=question,
    document_id=3,
    owner_id=2,
    top_k=3,
)

print("Question:", question)
print("Retrieved chunks:", len(results))

for index, chunk in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print("Source page:", chunk["page_number"])
    print("Text:", chunk["text"])
    print("Distance:", round(chunk["distance"], 4))