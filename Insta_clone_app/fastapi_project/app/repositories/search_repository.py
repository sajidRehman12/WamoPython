from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
from app.models.tables import Follow, User  
# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 
class searchRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_users(self, query: str, exclude_user_id: int, limit: int, offset: int) -> List[User]:
        
        search_filter = f"%{query}%"
        return (
            self.db.query(User)
            .filter(
                and_(
                    or_(
                        User.username.ilike(search_filter),
                    ),
                    User.id != exclude_user_id
                )
            )
            .offset(offset)
            .limit(limit)
            .all()
        )