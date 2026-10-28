
from rag_service import answer_question

question = "What technologies are listed in this resume?"

result = answer_question(
    question=question,
    document_id=3,
    owner_id=2,
    top_k=3,
)

print("Question:", question)
print("\nAnswer:")
print(result["answer"])
print("\nSource pages:", result["sources"])
