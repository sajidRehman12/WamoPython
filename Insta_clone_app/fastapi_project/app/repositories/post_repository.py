# app/repositories/post_repository.py

from sqlalchemy.orm import Session
from app.models.tables import Post
from app.models.tables import User
from fastapi import HTTPException
from app.models.tables import Follow
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
    def get_by_id(self, post_id: str, curr_user_id: str):
        clean_post_id = post_id.strip()
        post = self.db.query(Post).filter(Post.id == clean_post_id).first()
        if not post:
            return None 
        if post.user_id == curr_user_id:
            return post
        is_following = self.db.query(Follow).filter(
            Follow.follower_id == curr_user_id,
            Follow.following_id == post.user_id
        ).first()

        if is_following:
            return post
        return None

    def get_posts_by_user_id(self, user_id):
        return self.db.query(Post).filter(Post.user_id==user_id).all()
    

    def delete(self, post: Post):
        self.db.delete(post)
        self.db.commit()