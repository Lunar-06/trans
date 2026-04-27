from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session, joinedload
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
import json

from database import get_db
from models import User, Post, Comment
from schemas import PostCreate, PostResponse, CommentResponse, UserResponse
from auth import get_current_active_user

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=List[PostResponse])
@limiter.limit("30/minute")
async def get_posts(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取帖子列表 - 只返回公开的帖子，或者当前用户自己的帖子"""
    # 查询条件：公开帖子 或者 当前用户自己的帖子
    query = db.query(Post).options(joinedload(Post.comments))
    query = query.filter((Post.is_public == True) | (Post.author_id == current_user.id))
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    post_responses = []
    for post in posts:
        post_dict = {**post.__dict__}
        if post.images:
            post_dict["images"] = json.loads(post.images)
        else:
            post_dict["images"] = []
        post_dict["author"] = UserResponse.from_orm(post.author)
        post_dict["comments"] = [CommentResponse.from_orm(c) for c in post.comments]
        post_responses.append(PostResponse(**post_dict))
    
    return post_responses

@router.post("/", response_model=PostResponse)
@limiter.limit("10/minute")
async def create_post(
    request: Request,
    post_data: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新帖子"""
    if not post_data.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="帖子标题不能为空")
    
    if not post_data.content.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="帖子内容不能为空")
    
    images_json = json.dumps(post_data.images) if post_data.images else None
    
    post = Post(
        title=post_data.title,
        content=post_data.content,
        category=post_data.category,
        images=images_json,
        author_id=current_user.id,
        is_public=post_data.is_public if post_data.is_public is not None else True
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    post_dict = {**post.__dict__}
    post_dict["images"] = post_data.images
    post_dict["author"] = UserResponse.from_orm(current_user)
    post_dict["comments"] = []
    
    return PostResponse(**post_dict)

@router.get("/{post_id}", response_model=PostResponse)
@limiter.limit("30/minute")
async def get_post(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取单个帖子详情 - 只允许查看公开的帖子，或者当前用户自己的帖子"""
    post = db.query(Post).options(joinedload(Post.comments)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="帖子不存在")
    
    # 检查可见性：公开帖子 或者 当前用户自己的帖子
    if not post.is_public and post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="您无权查看此帖子")
    
    post_dict = {**post.__dict__}
    if post.images:
        post_dict["images"] = json.loads(post.images)
    else:
        post_dict["images"] = []
    post_dict["author"] = UserResponse.from_orm(post.author)
    post_dict["comments"] = [CommentResponse.from_orm(c) for c in post.comments]
    
    return PostResponse(**post_dict)

@router.post("/{post_id}/like")
@limiter.limit("10/minute")
async def like_post(
    request: Request,
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """点赞帖子 - 只允许点赞公开的帖子，或者当前用户自己的帖子"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="帖子不存在")
    
    # 检查可见性：公开帖子 或者 当前用户自己的帖子
    if not post.is_public and post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="您无权查看此帖子")
    
    post.likes += 1
    db.commit()
    
    return {"message": "点赞成功", "likes": post.likes}

@router.post("/{post_id}/comments", response_model=CommentResponse)
@limiter.limit("10/minute")
async def add_comment(
    request: Request,
    post_id: int,
    comment_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """添加评论 - 只允许评论公开的帖子，或者当前用户自己的帖子"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="帖子不存在")
    
    # 检查可见性：公开帖子 或者 当前用户自己的帖子
    if not post.is_public and post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="您无权查看此帖子")
    
    content = comment_data.get("content", "").strip()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="评论内容不能为空")
    
    comment = Comment(
        content=content,
        post_id=post_id,
        user_id=current_user.id,
        username=current_user.username,
        avatar=current_user.avatar or "👤"
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return CommentResponse.from_orm(comment)

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
@limiter.limit("30/minute")
async def get_comments(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取帖子的评论列表 - 只允许查看公开帖子的评论，或者当前用户自己帖子的评论"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="帖子不存在")
    
    # 检查可见性：公开帖子 或者 当前用户自己的帖子
    if not post.is_public and post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="您无权查看此帖子")
    
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    return [CommentResponse.from_orm(c) for c in comments]
