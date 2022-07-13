from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

# POSTS
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


# USERS
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

# LOGIN
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

# data that we gave to the token (such as id, email, etc)
class TokenData(BaseModel):
    id: Optional[str]