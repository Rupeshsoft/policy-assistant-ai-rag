# Refactoring Plan - Policy Assistant AI App

## ✅ Completed Steps
- [x] Analysis of existing codebase completed
- [x] Plan approved by user
- [x] Create `app/auth/roles.py` — extracted `admin_required()` and `role_required()` dependencies
- [x] Refactor `app/auth/security.py` — removed self-import, broken imports, and duplicate code
- [x] Create `app/routers/admin.py` — admin dashboard endpoint using proper dependency injection
- [x] Update `app/main.py` — included auth & admin routers, added CORS middleware
- [x] Create `.env.example` — documented required environment variables
- [x] Fix `app/models/user.py` — replaced broken `click.DateTime` import with proper SQLAlchemy `DateTime`

## 🔲 Next Steps (Manual)
1. [ ] Copy `.env.example` to `.env` and fill in your database credentials and JWT secret
2. [ ] Install dependencies: `pip install -r requirements.txt`
3. [ ] Run database creation: `python app/create_tables.py`
4. [ ] Start server: `uvicorn app.main:app --reload`
5. [ ] Test endpoints via Swagger UI at `http://localhost:8000/docs`

