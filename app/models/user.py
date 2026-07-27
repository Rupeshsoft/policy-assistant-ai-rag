from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id=Column(Integer,primary_key=True,index=True)

    fullname=Column(String(100))

    email=Column(String(100),unique=True)

    mobile=Column(String(20),unique=True)

    password=Column(String(255))

    role=Column(String(20),default="USER")

    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
