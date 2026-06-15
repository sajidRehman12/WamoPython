from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.feed_service import FeedService
from app.repositories.feed_repository import FeedRepository
from app.core.oauth import get_current_user  # your auth dependency

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/")
def get_feed(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    # user_id: str = Depends(get_current_user),
):
    repo = FeedRepository(db)
    service = FeedService(repo)

    return service.get_feed(
        # user_id.id
        "226497be-6fb2-428c-ab71-f4734a900916"
                            , limit, offset)