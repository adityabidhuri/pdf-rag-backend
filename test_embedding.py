
from embedding_service import embed_text

sample_text = (
    "The LIC loan interest payment was 8693 rupees."
)

vector = embed_text(sample_text)

print("Embedding generated successfully")
print("Vector type:", type(vector).__name__)
print("Vector dimensions:", len(vector))
print("First 10 values:", vector[:10])
