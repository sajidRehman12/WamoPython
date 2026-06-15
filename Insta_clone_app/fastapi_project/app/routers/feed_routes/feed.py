from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.feed_service import FeedService
from app.repositories.feed_repository import FeedRepository
from app.core.oauth import get_current_user  # your auth dependency
from app.schemas.post import PostResponse
router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/")
def get_feed(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    repo = FeedRepository(db)
    service = FeedService(repo)

    posts= service.get_feed(
        current_user.id, limit, offset)
    
    return [
    PostResponse(**row._mapping)
    for row in posts
        ]

    