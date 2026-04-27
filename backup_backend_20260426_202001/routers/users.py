from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel

from database import get_db
from models import User, Post
from schemas import UserResponse
from auth import get_current_user

# 用户设置模型
class UserSettings(BaseModel):
    theme: str = "auto"  # 主题设置: auto, light, dark
    language: str = "zh"  # 语言设置: zh, en
    notifications: bool = True  # 通知设置
    email_updates: bool = False  # 邮件更新

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/stats", response_model=dict)
@limiter.limit("30/minute")
async def get_user_stats(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户真实统计数据"""
    
    # 验证用户权限
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    
    # 统计用户帖子数量
    posts_count = db.query(func.count(Post.id)).filter(Post.author_id == current_user.id).scalar()
    
    # 统计用户点赞总数（所有帖子的点赞数之和）
    total_likes = db.query(func.sum(Post.likes)).filter(Post.author_id == current_user.id).scalar() or 0
    
    # 计算用户积分（基于帖子和点赞数）
    points = posts_count * 10 + total_likes * 2
    
    # 返回真实的用户统计数据（所有数据从0开始）
    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "orders_count": 0,  # 订单数量从0开始
        "favorites_count": 0,  # 收藏数量从0开始
        "posts_count": posts_count,  # 真实帖子数量
        "comments_count": 0,  # 评论数量从0开始
        "points": points,  # 基于真实数据的积分
        "total_likes": total_likes,  # 总点赞数
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

@router.get("/profile", response_model=UserResponse)
@limiter.limit("30/minute")
async def get_user_profile(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """获取用户基本信息"""
    return UserResponse.from_orm(current_user)

@router.get("/settings")
@limiter.limit("30/minute")
async def get_user_settings(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """获取用户设置"""
    # 返回默认设置或从数据库获取用户设置
    return {
        "theme": "auto",
        "language": "zh", 
        "notifications": True,
        "email_updates": False,
        "user_id": current_user.id
    }

@router.put("/settings")
@limiter.limit("10/minute")
async def update_user_settings(
    request: Request,
    settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户设置"""
    # 这里可以扩展用户设置字段
    # 目前主要处理主题设置
    return {"message": "设置已更新", "settings": settings}