from sqlalchemy.orm import Session
from app.models.tables import Post
from app.models.tables import Follow


class FeedRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_feed(self, user_id: str, limit: int = 20, offset: int = 0):
        followed_users = (
            self.db.query(Follow.following_id)
            .filter(Follow.follower_id == user_id)
            .subquery()
        )

        posts = (
            self.db.query(Post)
            .filter(
                (Post.user_id == user_id) |
                (Post.user_id.in_(followed_users)),
                 Post.is_published==True
                
            )
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return posts