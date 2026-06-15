from uuid import UUID 
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from app.models.tables import Story
from fastapi import HTTPException
from app.repositories.story_repository import StoryRepository
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png",".mp4"}

UPLOAD_DIR = Path("stories")
UPLOAD_DIR.mkdir(exist_ok=True)
BASE_URL = "http://localhost:8000/static/stories"

class StoryService:

    def __init__(
        self,
        story_repo :StoryRepository,
        notification_service
    ):
        self.story_repo = story_repo
        self.notification_service = notification_service

    async def save_story(self,file):
        extension = Path(file.filename).suffix
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type"
            )
       
        filename = f"{uuid.uuid4()}{extension}"
        file_path = UPLOAD_DIR / filename
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

        return f"{BASE_URL}/{filename}" 
    
    def get_stories_of_followings(self,user_id):
        return self.story_repo.get_stories_of_followings(user_id)

    def create_story(
        self,
        user_id: int,
        media_url: str,
        media_type: str
    ):
        story = Story(
            user_id=user_id,
            media_url=media_url,
            media_type=media_type,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        return self.story_repo.create(story)

    def get_active_stories(self):
        return self.story_repo.get_active_stories()

    def get_user_stories(self, user_id: int):
        return self.story_repo.get_user_stories(user_id)

    def delete_story(self, story_id: int, user_id: int):
        story = self.story_repo.get_by_id(story_id)
        if not story:
            raise ValueError("Story not found")
        if story.user_id != user_id:
            raise PermissionError("Not allowed to delete this story")
        self.story_repo.delete(story)
        return {"message": "Story deleted successfully"}
    

