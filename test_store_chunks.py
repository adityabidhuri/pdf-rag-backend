
from pathlib import Path

from pdf_service import extract_pdf_text
from chunking_service import chunk_pages
from vector_store import collection, store_chunks

pdf_files = list(Path("uploads").glob("*.pdf"))

if not pdf_files:
    print("No PDF files found in uploads/")
else:
    pdf_path = pdf_files[0]

    # Step 1: Extract PDF text
    pages = extract_pdf_text(str(pdf_path))

    # Step 2: Split the text into chunks
    chunks = chunk_pages(pages)

    # Step 3: Generate embeddings and store the chunks
    stored_count = store_chunks(
        chunks=chunks,
        document_id=999999,
        owner_id=999999,
    )

    print("PDF:", pdf_path.name)
    print("Chunks prepared:", len(chunks))
    print("Chunks processed:", stored_count)
    print("Total records in collection:", collection.count())
