# Run locally

## Frontend

**Option A** — install once in the app folder (recommended):

```powershell
cd frontend\agent
npm install
npm run dev
```

**Option B** — from `frontend/` (forwards to `agent/`):

```powershell
cd frontend
npm run install:app
npm run dev
```

## Agentic RAG API

Run from **`RAG`** (parent of the `agentic_rag` package). Do **not** `cd` into `agentic_rag` itself.

```powershell
cd C:\Users\nakul.maheshwari\agentic_rag_full\RAG
$env:PYTHONUTF8 = "1"
uvicorn agentic_rag.api.main:app --reload
```

`PYTHONUTF8` avoids Windows console errors from emoji in log output.

## Ingestion API

From `RAG/ingestion_pipeline`:

```powershell
cd ingestion_pipeline
uvicorn api.main:app --port 8080 --reload
```
