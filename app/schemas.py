from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


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

# POSTS
class Post(BaseModel):
    title: str
    content: str
    published: bool

class PostBase(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True



class PostVote(BaseModel):
    Post: PostBase
    votes: int

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


# VOTING
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # less than 1
