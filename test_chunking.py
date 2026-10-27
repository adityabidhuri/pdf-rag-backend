
from pathlib import Path

from pdf_service import extract_pdf_text
from chunking_service import chunk_pages

pdf_files = list(Path("uploads").glob("*.pdf"))

if not pdf_files:
    print("No PDF files found in uploads/")
else:
    pdf_path = pdf_files[0]

    pages = extract_pdf_text(str(pdf_path))
    chunks = chunk_pages(pages)

    print("PDF:", pdf_path.name)
    print("Pages with extractable text:", len(pages))
    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks[:5], start=1):
        print(f"\n--- Chunk {index} ---")
        print("Source page:", chunk["page_number"])
        print("Characters:", len(chunk["text"]))
        print(chunk["text"])
