from fastapi import Depends, HTTPException
from app.auth.security import get_current_user


def admin_required(current_user: dict = Depends(get_current_user)):
    """Dependency to ensure the current user has ADMIN role."""
    if current_user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admin privileges required."
        )
    return current_user


def role_required(required_role: str):
    """Factory function to create role-checking dependencies for any role."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. '{required_role}' role required."
            )
        return current_user
    return role_checker

