from uuid import UUID
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status,UploadFile ,File
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.oauth import get_current_user

from app.repositories.story_repository import StoryRepository
from app.repositories.notification_repository import NotificationRepository

from app.services.story_service import StoryService
from app.services.notification_service import NotificationService


router = APIRouter(prefix="/stories", tags=["Stories"])

def get_story_service(db: Session = Depends(get_db)):
    return StoryService(
        StoryRepository(db),
        NotificationService(NotificationRepository(db))
    )

@router.post("/")
async def create_story(
    file: UploadFile = File(...),
    # current_user=Depends(get_current_user),
    service: StoryService = Depends(get_story_service)
):
    media_url=await service.save_story(file)
    media_type=Path(file.filename).suffix

    try:
        return service.create_story(
            # user_id=current_user.id,
            user_id="226497be-6fb2-428c-ab71-f4734a900916",
            media_url=media_url,
            media_type=media_type
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.get("/active")
def get_active_stories(
    service: StoryService = Depends(get_story_service)
):
    return service.get_active_stories()

@router.get("/user/{user_id}")
def get_user_stories(
    user_id: UUID,
    service: StoryService = Depends(get_story_service)
):
    return service.get_user_stories(user_id)

@router.delete("/{story_id}")
def delete_story(
    story_id: UUID,
    current_user=Depends(get_current_user),
    service: StoryService = Depends(get_story_service)
):
    try:
        return service.delete_story(story_id, current_user.id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
