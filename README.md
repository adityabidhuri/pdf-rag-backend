# PDF RAG Backend

A backend application built with **FastAPI** that allows authenticated users to upload PDF documents and ask questions about their content using Retrieval-Augmented Generation (RAG).

The application extracts text from PDFs, splits it into smaller chunks, generates embeddings, stores them in ChromaDB, retrieves relevant context for a question, and uses Google's Gemini API to generate an answer grounded in the document.

## Features

- **User authentication:** Registration and login with hashed passwords and JWT-based authentication.
- **PDF upload:** Upload PDF documents through a REST API.
- **Document management:** List, retrieve, and delete a user's uploaded documents.
- **PDF text extraction:** Extract text and preserve page numbers using `pypdf`.
- **Text chunking:** Split extracted text into smaller, overlapping chunks.
- **Embeddings:** Generate vector embeddings using Google's Gemini API.
- **Vector database:** Store and search document chunks using ChromaDB.
- **Question answering:** Retrieve relevant chunks and generate answers using Gemini.
- **Source pages:** Return source page numbers alongside generated answers.
- **API documentation:** Interactive API documentation through Swagger UI.

## Tech Stack

- **Language:** Python
- **API framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Authentication:** JWT and Argon2 password hashing
- **PDF processing:** pypdf
- **Embeddings and generation:** Google Gemini API
- **Vector database:** ChromaDB
- **Environment configuration:** python-dotenv

## How RAG Works

1. A user registers and logs in to receive an access token.
2. The authenticated user uploads a PDF.
3. The backend extracts text and its page numbers.
4. The text is split into smaller chunks with overlap.
5. Gemini generates embeddings for the chunks.
6. ChromaDB stores the chunks, embeddings, and associated metadata.
7. The user submits a question about the uploaded document.
8. The backend retrieves relevant chunks using semantic similarity search.
9. The retrieved context and question are sent to Gemini.
10. The API returns the generated answer and source page numbers.

## Project Structure

```text
pdf-rag-backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── auth_service.py
├── documents.py
├── pdf_service.py
├── chunking_service.py
├── embedding_service.py
├── vector_store.py
├── rag_service.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The `tests/` directory is intended for the project's test and diagnostic scripts. Local runtime directories such as `uploads/` and `chroma_db/`, and the SQLite database file, are created or used locally and should not be committed.

## Prerequisites

- Python 3.11 or a compatible version supported by the installed dependencies
- A Google Gemini API key with access to the configured models
- Git

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd pdf-rag-backend
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root using `.env.example` as a template.

```dotenv
GEMINI_API_KEY=your_actual_api_key
```

Replace the placeholder with your own API key. Never commit `.env` or expose your API key in source code, screenshots, or logs.

### 5. Start the server

```powershell
uvicorn main:app --reload
```

Open the interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Log in and obtain an access token |
| GET | `/auth/me` | Get the authenticated user's information |
| POST | `/documents/upload` | Upload and process a PDF |
| GET | `/documents/` | List the current user's documents |
| GET | `/documents/{document_id}` | Retrieve a document's details |
| DELETE | `/documents/{document_id}` | Delete a document |
| POST | `/documents/{document_id}/ask` | Ask a question about a PDF |
| GET | `/` | Basic application endpoint |
| GET | `/health/database` | Check database connectivity |

Use `/docs` to inspect the actual request schemas, authentication requirements, and responses for each endpoint.

## Example: Ask a Question

Request:

```http
POST /documents/3/ask
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

```json
{
  "question": "Which technologies are listed in this document?"
}
```

Example response:

```json
{
  "answer": "The document lists FastAPI, REST APIs, Docker, and other technologies. (Source: Page 1)",
  "sources": [1]
}
```

The answer above is illustrative; actual answers depend on the uploaded document and retrieved context.

## Important Notes

- Only PDFs containing extractable text can be processed by the current text-extraction pipeline. Scanned PDFs may require OCR.
- AI-generated answers may be incomplete or inaccurate. Verify important information against the original document.
- Gemini API availability, latency, quotas, and model access can affect answer generation.
- Local SQLite data, uploaded documents, ChromaDB files, and secrets should remain outside version control.
- Production deployment should use secure secret management, appropriate file storage, and additional operational safeguards.

## Future Improvements

- Automated tests for authentication, document management, and RAG.
- Improved handling of scanned PDFs with OCR.
- More robust document-processing and AI retry strategies.
- Better observability and structured logging.
- Deployment configuration and production-ready storage.
- Evaluation of retrieval quality and answer grounding.

## License

ADITYA BIDHURI
