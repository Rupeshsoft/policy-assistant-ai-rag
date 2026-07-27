from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister
from app.auth.password import hash_password

from app.schemas.user import UserLogin
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token

router=APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register")
def register(user:UserRegister,db:Session=Depends(get_db)):

    existing=db.query(User).filter(User.email==user.email).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user=User(

        fullname=user.fullname,

        email=user.email,

        mobile=user.mobile,

        password=hash_password(user.password),

        role=user.role.upper()

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "message":"Registration Successful"
    }
    

@router.post("/login")

def login(user:UserLogin,db:Session=Depends(get_db)):

    db_user=db.query(User).filter(
        User.email==user.email
    ).first()

    if db_user is None:

        raise HTTPException(401,"Invalid Email")

    if not verify_password(user.password,db_user.password):

        raise HTTPException(401,"Invalid Password")

    token=create_access_token(

        {
            "sub":db_user.email,
            "role":db_user.role
        }

    )

    response_data = {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role
    }

    # If user is admin, include dashboard redirect
    if db_user.role == "ADMIN":
        response_data["redirect_url"] = "/admin/dashboard"

    return response_data
