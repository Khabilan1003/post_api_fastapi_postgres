from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Post Schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class CreatePost(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Posts: ResponsePost
    votes: int
    
    class Config:
        orm_mode = True

# User Schema
class CreateUser(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        
# Beared Token Schema
class BearerToken(BaseModel):
    access_token: str
    token_type: str
    
# Vote
class VoteBody(BaseModel):
    post_id: int
    dir: int