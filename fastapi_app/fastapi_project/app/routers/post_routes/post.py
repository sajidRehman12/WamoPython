# app/routers/post/post_router.py

from fastapi import APIRouter, Depends, HTTPException ,Request
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.post import PostCreate, PostResponse
from app.services.post_service import PostService
from app.repositories.post_repository import PostRepository
from app.core.oauth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = PostService(PostRepository(db))
    post = service.create_post(
        title=payload.title,
        content=payload.content,
        user_id=current_user.id
    )

    return post
    


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    service = PostService(PostRepository(db))
    return service.get_posts()



@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id, db: Session = Depends(get_db)):
    service = PostService(PostRepository(db))

    post = service.get_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.delete("/{post_id}")
def delete_post(
    post_id,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = PostService(PostRepository(db))

    post = service.get_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    service.delete_post(post)

    return {"message": "Post deleted"}