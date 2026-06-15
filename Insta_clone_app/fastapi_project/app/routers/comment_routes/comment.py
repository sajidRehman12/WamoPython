from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status ,Form
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.oauth import get_current_user
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.comment_service import CommentService
from app.services.notification_service import NotificationService


router = APIRouter(prefix="/comments", tags=["Comments"])

def get_comment_service(db: Session = Depends(get_db)):
    return CommentService(
        CommentRepository(db),
        PostRepository(db),
        NotificationService(NotificationRepository(db))
    )

@router.post("/{post_id}")
def create_comment(
    post_id: int,
    parent_id: int| None = Form(None),
    body: str = Form(...),
    current_user=Depends(get_current_user),
    service: CommentService = Depends(get_comment_service)
):
    print(parent_id)
    try:
        return service.create_comment(
            post_id=post_id,
            user_id=current_user.id,
            body=body,
            parent_id=parent_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.get("/post/{post_id}")
def get_comments(
    post_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = CommentRepository(db)
    return repo.get_by_post(post_id)


@router.get("/post/{post_id}/{comment_id}")
def get_comments(
    post_id: int,
    comment_id:int,
    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):
    repo = CommentRepository(db)
    return repo.get_by_post(post_id)



@router.get("/{comment_id}/replies")
def get_replies(
    comment_id: int,
    current_user=Depends(get_current_user),

    db: Session = Depends(get_db)
):
    repo = CommentRepository(db)
    return repo.get_replies(comment_id)

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user=Depends(get_current_user),
    service: CommentService = Depends(get_comment_service)
):
    try:
        return service.delete_comment(
            comment_id,
            current_user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

