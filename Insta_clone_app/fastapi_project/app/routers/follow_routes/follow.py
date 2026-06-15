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
    user_id: int,
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        service.follow_user(current_user.id, user_id)
        return {"message":"started following"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/follows")
def get_follow_list_of_user(
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        return service.get_following_list(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/followers")
def get_followers_list_of_user(
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        return service.get_followers_list(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/followslist")
def get_full_follow_list_of_user(
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        follows_list=service.get_full_list_following_list(current_user.id)
        return [{"username": follow.username,
                 "avatar_url": follow.avatar_url} for follow in follows_list]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/followerslist")
def get_full_followers_list_of_user(
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        follower_list= service.get_full_list_followers_list(current_user.id)
        return [{"username": follower.username,
                 "avatar_url": follower.avatar_url} for follower in follower_list]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def unfollow_user(
    user_id: int,
    current_user=Depends(get_current_user),
    service: FollowService = Depends(get_follow_service)
):
    try:
        return service.unfollow_user(current_user.id, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))