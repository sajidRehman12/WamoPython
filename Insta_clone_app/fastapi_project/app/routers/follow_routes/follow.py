from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_db
from app.core.oauth import get_current_user

from app.repositories.follow_repository import FollowRepository
from app.repositories.notification_repository import NotificationRepository

from app.services.follow_service import FollowService
from app.services.notification_service import NotificationService


router = APIRouter(prefix="/follows", tags=["Follows"])


def get_follow_service(db=Depends(get_db)):
    return FollowService(
        FollowRepository(db),
        NotificationService(NotificationRepository(db))
    )


@router.post("/{user_id}")
def follow_user(
    user_id: UUID,
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        return service.follow_user(current_user.id, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.delete("/{user_id}")
def unfollow_user(
    user_id: UUID,
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        return service.unfollow_user(current_user.id, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))