
def chunk_text(text: str,page_number: int,chunk_size: int = 800,overlap: int = 100,) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "page_number": page_number,
                "text": chunk,
            })

        start += chunk_size - overlap

    return chunks


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[dict]:
    all_chunks = []

    for page in pages:
        page_chunks = chunk_text(
            text=page["text"],
            page_number=page["page_number"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        all_chunks.extend(page_chunks)

    return all_chunks
