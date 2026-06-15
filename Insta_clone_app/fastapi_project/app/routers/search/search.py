from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.user import UserResponse
from app.core.oauth import get_current_user

# Import your new architectural layers
from app.repositories.search_repository import searchRepository
from app.services.search_service import searchService

router = APIRouter(prefix="/search", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def search_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    search_repository = searchRepository(db)
    search_service = searchService(search_repository)
    
    results = search_service.search_accounts(
        query=q,
        current_user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    
    return results