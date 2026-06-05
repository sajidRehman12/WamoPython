# app/repositories/post_repository.py

from sqlalchemy.orm import Session
from app.schemas.tables import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, post: Post):
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_all(self):
        return self.db.query(Post).all()

    def get_by_id(self, post_id):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def delete(self, post: Post):
        self.db.delete(post)
        self.db.commit()