from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from pathlib import Path
from fastapi import HTTPException
import uuid 
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

UPLOAD_DIR = Path("profile_pictures")
UPLOAD_DIR.mkdir(exist_ok=True)
BASE_URL = "http://localhost:8000/profile_pictures"

class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, username: str, email: str, password: str):

        if self.repo.get_by_username(username):
            raise Exception("Username already exists")

        if self.repo.get_by_email(email):
            raise Exception("Email already exists")

        from app.models.tables import User

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )

        return self.repo.create_user(user)

    def authenticate_user(self, username: str, password: str):

        user = self.repo.get_by_username(username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def get_user_by_id(self, user_id: str):
        return self.repo.get_by_id(user_id)

    def get_all_users(self):
        return self.repo.get_all()

    def delete_user(self, user_id: str):

        user = self.repo.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        self.repo.delete_user(user)
        return {"message": "User deleted successfully"}

    def update_user(self, user_id: str, data: dict):

        user = self.repo.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        return self.repo.update_user(user, data)
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
    
    
    def upload_profile_picture(self,user_id,url):
        self.repo.save_profile_picture(user_id=user_id,image_url= url)
        return "image saved successfully" 
    