

# app/routers/post/post_router.py
from fastapi import Form,APIRouter, Depends, HTTPException ,Request ,File ,UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.post import PostCreate, PostResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.core.oauth import get_current_user
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix="/user", tags=["users"])



@router.post("/upload-profile-photo")
async def upload_profile(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = UserService(UserRepository(db))
    url = await service.save_image(image)
    post = service.upload_profile_picture(user_id=current_user.id,url=url)
    return post
    
