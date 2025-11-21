# AI Test API

Lightweight FastAPI service for uploading documents, indexing them into a local Chroma store and answering questions using a RAG-style (retrieval-augmented generation) flow.

This README provides quick setup and run instructions, a short API reference (based on the code in `src/`), and simple examples to try locally.

## Table of contents

- What this is
- Prerequisites
- Quick setup
- Running the app
- API endpoints
- Examples
- Notes & next steps

## What this is

The project is a small API that exposes endpoints to:

- upload documents (`/upload`) for indexing
- trigger indexing (`/index`) — lightweight endpoint in the code
- chat with the indexed documents (`/chat`) using a RAG answerer
- download stored documents (`/docs/{id}`)

The service is implemented with FastAPI; the entrypoint is `src/main.py`.

## Prerequisites

- Python 3.11+ (3.13 is used in the development environment used to create this project)
- git (optional)
- Make sure you have a working virtual environment and `pip` available.

## Quick setup

1. Create or activate a virtual environment in the repo root. On Windows with Git Bash (or other bash):

```bash
python -m venv .venv
source Scripts/activate
```

On PowerShell:

```powershell
.\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file in the project root if your environment requires secrets or configuration. The code calls `dotenv.load_dotenv()` so any variables you add in `.env` will be loaded into the process environment. Inspect `src/services` and `src/db` if you need to know exact names of expected variables.

## Running the app

There are two common ways to start the service.

1) Using Uvicorn (recommended for development with reload):

```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
```

2) Or run the script directly (the file calls uvicorn when executed):

```bash
python src/main.py
```

The app listens on port 3000 by default. Once started, FastAPI's interactive docs are available (if enabled) at `/docs` and the OpenAPI spec at `/openapi.json`.

## API endpoints (quick reference)

Listed here are the endpoints implemented in `src/main.py`.

- POST /upload
  - Description: Upload a document (multipart file). The file will be processed and indexed.
  - Request: multipart/form-data with `file` field (UploadFile)
  - Response: JSON with status and indexing ids

- POST /index
  - Description: Lightweight endpoint present in the code (returns `True`).

- POST /chat
  - Description: Ask a question; the service will use a RAG pipeline to answer based on uploaded documents.
  - Request JSON schema (based on `src/models/chat.py`):

```json
{
  "user_id": "string",
  "message": "your question here",
  "doc_id": ["optional-document-id-1", "optional-document-id-2"]
}
```

  - Response schema (`ChatResponse`):

```json
{
  "response": "answer text",
  "message_id": "string",
  "created_at": 1700000000000
}
```

- GET /docs/{id}
  - Description: Download or retrieve the stored document content by id.
  - Response: JSON with the document data under `data`.

## Examples

1) Example `curl` to call `/chat` (replace host/port if needed):

```bash
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test-user","message":"Summarize the uploaded document","doc_id":null}'
```

2) File upload example to `/upload` using `curl`:

```bash
curl -X POST http://localhost:3000/upload \
  -F "file=@/path/to/document.pdf"
```

## Notes & next steps

- The code already imports `dotenv` and attempts to use a Mongo collection (`db.mongo`) and other services in `src/services/`. If the services require configuration (API keys, connection strings), add them to `.env`.
- There are no automated tests included in the repository root. Consider adding a minimal test suite (pytest) and a `Makefile` or `tasks` to simplify local dev commands.
- Recommended improvements:
  - Document required environment variables explicitly (inspect `src/services` and `src/db`)
  - Add example payloads for `/upload` responses and sample data in `chroma_store/`
  - Add CONTRIBUTING.md and LICENSE if you plan to share or accept contributions

## Where to look next in the repo

- `src/main.py` — main FastAPI app and endpoints
- `src/models/` — Pydantic models (e.g., `chat.py`)
- `src/services/` — LLM client, upload/index/download, and RAG logic
- `chroma_store/` — local Chroma DB files (vector index files)
- `requirements.txt` — Python dependencies