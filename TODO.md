# Fix 401 "Not authenticated" on /documents/upload

## Steps

### ✅ Step 1: Update `app/auth/security.py`
- Add `get_token_from_form_or_query()` function to extract token from form field or query param ✅
- Add `get_current_user_flexible()` dependency that tries multiple ways to get the token ✅
- Keep original `get_current_user` unchanged for other endpoints ✅

### ✅ Step 2: Update `app/routers/document.py`
- Modify upload endpoint to use `get_current_user_flexible()` instead of `get_current_user()` ✅ (REVERTED)
- **NEW FIX**: Replaced `get_current_user_flexible` with a dedicated `_resolve_upload_user` dependency that:
  - Uses `oauth2_scheme` (Authorization header) as a proper FastAPI dependency
  - Accepts an explicit `form_token: str = Form(None)` parameter (no stream conflict)
  - Falls back to `request.query_params.get("token")` for query param support
  - Calls `_validate_token_and_get_user()` from security.py for JWT validation

### ✅ Step 3: Create test script
- Add `test_upload.py` to test the full flow end-to-end ✅

### ✅ Step 4: Test
- Run the test script to verify the fix ✅
- All 4 tests pass: Auth Header ✅, Form Field ✅, Query Param ✅, No Auth (401) ✅

