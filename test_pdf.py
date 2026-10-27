
from pathlib import Path
from pdf_service import extract_pdf_text

# Find PDF files inside the uploads folder
pdf_files = list(Path("uploads").glob("*.pdf"))

if not pdf_files:
    print("No PDF files found in the uploads folder.")
else:
    # Select the first PDF found
    pdf_path = pdf_files[0]

    # Extract text from the PDF
    pages = extract_pdf_text(str(pdf_path))

    print("File:", pdf_path.name)
    print("Pages containing text:", len(pages))

    # Display text from the first two pages
    for page in pages:
        print(f"\n--- Page {page['page_number']} ---")
        print("Characters extracted:", len(page["text"]))
        print(page["text"])
