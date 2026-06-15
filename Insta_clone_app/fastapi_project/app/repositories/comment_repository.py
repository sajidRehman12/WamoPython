from uuid import UUID
from sqlalchemy.orm import Session

from app.models.tables import Comment


class CommentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: Comment):
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_by_id(self, comment_id: UUID):
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    def get_by_post(self, post_id: UUID):
        return (
            self.db.query(Comment)
            .filter(
                Comment.post_id == post_id,
                Comment.parent_id == None
            )
            .order_by(Comment.created_at.desc())
            .all()
        )

    def get_replies(self, parent_id: UUID):
        return (
            self.db.query(Comment)
            .filter(Comment.parent_id == parent_id)
            .order_by(Comment.created_at.asc())
            .all()
        )


    def delete(self, comment: Comment):
        self.db.delete(comment)
        self.db.commit()