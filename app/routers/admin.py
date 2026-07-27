from fastapi import APIRouter, Depends
from app.auth.roles import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def admin_dashboard(current_user: dict = Depends(admin_required)):
    """Admin-only dashboard endpoint."""
    return {
        "message": "Welcome Admin",
        "user": current_user
    }

