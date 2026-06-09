# app/services/post_service.py

from app.models.tables import Post
from app.repositories.post_repository import PostRepository
from pathlib import Path
import uuid
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
BASE_URL = "http://localhost:8000/uploads"

class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo
    async def save_image(self,file):
        extension = Path(file.filename).suffix
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type"
            )
        filename = f"{uuid.uuid4()}{extension}"
        file_path = UPLOAD_DIR / filename
        content = await file.read()
        file_path.write_bytes(content)
        return f"{BASE_URL}/{filename}" 
    
    def create_post(self, title: str,url: str, user_id,publish_status:bool = True,publish_time:Optional[datetime] = datetime.now()):
        
        sheduled_at= None
        published_at= None
        if publish_status is False:
            sheduled_at=publish_time
        else:
            published_at=publish_time
        post = Post(
            caption=title,
            user_id=user_id,
            image_url=url,
            is_published=publish_status,
            scheduled_at=sheduled_at,
            published_at=published_at
        )
        return self.repo.create(post)
  
    def get_posts_by_user_id(self,user_id):

        return self.repo.get_posts_by_user_id(user_id)

    def get_posts(self):
        return self.repo.get_all()


    def get_post(self, post_id ,curr_user_id):
        post= self.repo.get_by_id(post_id,curr_user_id)
        if post is None:     
            raise HTTPException(
                status_code=404,
                detail="Post not authorized to view"
            )
        return post

    def delete_post(self, post):
        return self.repo.delete(post)