from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.oauth import get_current_user
from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.like_service import LikeService
from app.services.notification_service import NotificationService
from app.schemas.like import LikeWithUsername

router = APIRouter(prefix="/like", tags=["likes"])

def get_like_service(db: Session = Depends(get_db)):
    return LikeService(
        LikeRepository(db),
        PostRepository(db),
        NotificationService(NotificationRepository(db))
    )

@router.post("/{post_id}")
def add_like(
    post_id: int,
    current_user=Depends(get_current_user),
    service: LikeService = Depends(get_like_service)
):
    try:
        service.like_post(
            post_id=post_id,
            user_id=current_user.id,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return{"message":"post liked successfully"}

@router.delete("/{post_id}")
def delete_like(
    post_id:int,
    current_user=Depends(get_current_user),
    service: LikeService = Depends(get_like_service)
):
    try:
        return service.unlike_post(
            post_id=post_id,
            user_id=current_user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.get("/post/{post_id}"  )
def likes_on_a_post(
    post_id:int,
    current_user=Depends(get_current_user),
    service: LikeService = Depends(get_like_service)
):
    try:
        likes= service.likes_on_a_post(
            post_id=post_id,
        )
        return likes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

