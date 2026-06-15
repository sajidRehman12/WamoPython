from uuid import UUID
from sqlalchemy.orm import Session

from app.models.tables import Follow


class FollowRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, follow: Follow):
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def get_follow(self, follower_id: UUID, following_id: UUID):
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

    def get_following(self, user_id: UUID):
        return (
            self.db.query(Follow)
            .filter(Follow.follower_id == user_id)
            .all()
        )

    def get_followers(self, user_id: UUID):
        return (
            self.db.query(Follow)
            .filter(Follow.following_id == user_id)
            .all()
        )

    def count_following(self, user_id: UUID):
        return (
            self.db.query(Follow)
            .filter(Follow.follower_id == user_id)
            .count()
        )

    def count_followers(self, user_id: UUID):
        return (
            self.db.query(Follow)
            .filter(Follow.following_id == user_id)
            .count()
        )