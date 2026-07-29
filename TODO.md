# Fix Issues in Policy Assistant AI App

## Steps

### ✅ Step 1: Fix `app/routers/document.py`
- [x] Remove duplicate router definitions (keep only `/documents` prefix)
- [x] Fix duplicate route paths for POST `/{document_id}` → `/extract`, `/chunk`, `/embeddings`
- [x] Add missing `os` import
- [x] Add missing `ChunkingService` and `ChunkStorageService` imports

### ✅ Step 2: Fix `app/services/docx_reader.py`
- [x] Change `"paragraph"` key to `"page"` key to match ChunkingService expectations

### ✅ Step 3: Update `requirements.txt`
- [x] Add missing dependencies (nltk, sentence-transformers, transformers, chromadb, PyMuPDF, python-docx, ollama, httpx)

### ✅ Step 4: Fix `datetime.utcnow()` deprecation
- [x] Fix `app/auth/jwt_handler.py` - switched to `datetime.now(timezone.utc)`
- [x] Fix `app/services/chunking_service.py` - switched to `datetime.now(timezone.utc)`

### ✅ Step 5: Fix duplicate line in `app/create_tables.py`
- [x] Remove duplicate `Base.metadata.create_all(bind=engine)` call

### ✅ Step 6: Add NLTK punkt download handling
- [x] Add punkt auto-download in chunking_service.py via `nltk.download("punkt")`

## All Issues Fixed ✅
