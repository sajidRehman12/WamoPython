from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.tables import Story


class StoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, story: Story):
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story

    def get_by_id(self, story_id: UUID):
        return (
            self.db.query(Story)
            .filter(Story.id == story_id)
            .first()
        )

    def get_active_stories(self):
        return (
            self.db.query(Story)
            .filter(Story.expires_at > datetime.utcnow())
            .order_by(Story.created_at.desc())
            .all()
        )

    def get_user_stories(self, user_id: UUID):
        return (
            self.db.query(Story)
            .filter(Story.user_id == user_id)
            .order_by(Story.created_at.desc())
            .all()
        )

    def delete(self, story: Story):
        self.db.delete(story)
        self.db.commit()