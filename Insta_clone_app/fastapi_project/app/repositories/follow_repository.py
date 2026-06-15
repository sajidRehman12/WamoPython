
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.tables import Follow,User
# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 

class FollowRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, follow: Follow):
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def get_follow(self, follower_id: int, following_id: int):
        return (
            self.db.query(Follow)
            .filter(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id
            )
            .first()
        )

    def delete(self, follow: Follow):
        self.db.delete(follow)
        self.db.commit()

    def get_following(self, user_id: int):
        return (
            self.db.query(Follow)
            .filter(Follow.follower_id == user_id)
            .all()
        )

    def get_followers(self, user_id: int):
        return (
            self.db.query(Follow)
            .filter(Follow.following_id == user_id)
            .all()
        )

    def count_following(self, user_id: int):
        
        
        return (
            self.db.query(Follow)
            .filter(Follow.follower_id == user_id)
            .count()
        )

    def count_followers(self, user_id: int):
        

        return (
            self.db.query(Follow)
            .filter(Follow.following_id == user_id)
            .count()
        )
    

    def list_following(self, user_id: int):
        return self.db.query(User.username,User.avatar_url).join(Follow, Follow.following_id == User.id).filter(Follow.follower_id == user_id).all()

        stmt = (
                select(User.username)
                .join(Follow, Follow.following_id == User.id)
                .filter(Follow.follower_id == user_id)
            )
        return self.db.execute(stmt).all()

    def list_followers(self, user_id: int):
        
        return self.db.query(User.username,User.avatar_url).join(Follow, Follow.follower_id == User.id).filter(Follow.following_id == user_id).all()
        stmt = (
                select(User.username)
                .join(Follow, Follow.follower_id == User.id)
                .filter(Follow.following_id == user_id)
            )
        return self.db.execute(stmt).all()

        