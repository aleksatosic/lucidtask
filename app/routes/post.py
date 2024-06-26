from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from cachetools import cached, TTLCache
from app.schemas.post import PostCreate, Post
from app.crud.post import create_post, get_posts, delete_post
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.user import User

router = APIRouter()

cache = TTLCache(maxsize=100, ttl=300)


@router.post("/posts", response_model=Post)
def add_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if len(post.text.encode("utf-8")) > 1 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload too large")
    return create_post(db=db, post=post, user_id=current_user.id)


@router.get("/posts", response_model=List[Post])
@cached(cache)
def get_user_posts(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_posts(db=db, user_id=current_user.id)


@router.delete("/posts/{post_id}")
def delete_user_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = delete_post(db=db, post_id=post_id)
    if not post or post.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
