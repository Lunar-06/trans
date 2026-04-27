from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str] = "🧑"

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度至少6位')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class PostBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = "travel"
    images: Optional[List[str]] = []
    is_public: Optional[bool] = True  # 默认公开可见

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    author: UserResponse
    likes: int
    is_liked: bool
    is_public: bool
    created_at: datetime
    updated_at: datetime
    comments: List['CommentResponse'] = []
    
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    username: str
    avatar: str
    created_at: datetime
    
    class Config:
        from_attributes = True