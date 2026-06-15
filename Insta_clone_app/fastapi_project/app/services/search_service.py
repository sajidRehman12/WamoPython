from typing import List
from app.repositories.search_repository import searchRepository
from app.models.tables import User
# from app.models import user
class searchService:
    def __init__(self, user_repo: searchRepository):
        self.user_repo = user_repo

    def search_accounts(self, query: str, current_user_id: int, limit: int, offset: int) -> List[User]:
        
        cleaned_query = query.strip()
        
        if not cleaned_query:
            return []
            
        return self.user_repo.search_users(
            query=cleaned_query,
            exclude_user_id=current_user_id,
            limit=limit,
            offset=offset
        )