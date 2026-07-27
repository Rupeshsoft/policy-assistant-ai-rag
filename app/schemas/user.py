from pydantic import BaseModel,EmailStr

class UserRegister(BaseModel):

    fullname:str

    email:EmailStr

    mobile:str

    password:str

    role:str="USER"


class UserLogin(BaseModel):

    email:str

    password:str


class UserResponse(BaseModel):

    id:int

    fullname:str

    email:str

    mobile:str

    role:str

    class Config:
        from_attributes=True