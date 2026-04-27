from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

def local_now():
    """返回本地当前时间"""
    return datetime.now()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(10), default="🧑")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=local_now)
    updated_at = Column(DateTime, default=local_now, onupdate=local_now)
    
    # 关系
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(20), default="travel")
    images = Column(Text)  # 存储图片URL列表的JSON字符串
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    likes = Column(Integer, default=0)
    is_liked = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)  # 帖子可见性，默认公开
    created_at = Column(DateTime, default=local_now)
    updated_at = Column(DateTime, default=local_now, onupdate=local_now)
    
    # 关系
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String(50), nullable=False)
    avatar = Column(String(10), default="👤")
    created_at = Column(DateTime, default=local_now)
    
    # 关系
    post = relationship("Post", back_populates="comments")
    user = relationship("User")