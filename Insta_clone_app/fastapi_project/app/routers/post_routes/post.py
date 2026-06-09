# app/routers/post/post_router.py
from fastapi import Form,APIRouter, Form,Depends, HTTPException ,Request ,File ,UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import PostService
from app.repositories.post_repository import PostRepository
from app.core.oauth import get_current_user
from fastapi.staticfiles import StaticFiles
from datetime import datetime ,timezone
from app.schemas.post import PostCreate
from pydantic import Json
from typing import Annotated

from pydantic import field_validator,BaseModel

router = APIRouter(prefix="/posts", tags=["Posts"])

# @router.post("/date-time")
# def datetimerouter(data: DateInput):
#     return data


@router.post("/")
async def create_post(
    post: Annotated[Json[PostCreate], Form()],
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    
    service = PostService(PostRepository(db))
    image_path= await service.save_image(image)
    publish_status=True
    published_at = post.event_date.astimezone(timezone.utc)

    if post.event_date is not None:
        if published_at >= datetime.now(timezone.utc):
            publish_status= False 
    else:
        published_at=datetime.now(timezone.utc)
    post = service.create_post(
        title=post.title,
        user_id="226497be-6fb2-428c-ab71-f4734a900916",
        url=image_path,
        publish_status=publish_status,
        publish_time=published_at
    )
    return post
    
@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db),   
               current_user = Depends(get_current_user)
):
    service = PostService(PostRepository(db))
    return service.get_posts()

@router.get("/user/posts")
def get_posts_by_user( db: Session = Depends(get_db)
                      , current_user = Depends(get_current_user)):
    service = PostService(PostRepository(db))
    return service.get_posts_by_user_id(current_user.id)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id, 
            db: Session = Depends(get_db),  
            current_user = Depends(get_current_user)
):
    service = PostService(PostRepository(db))
    post = service.get_post(post_id,current_user.id)
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