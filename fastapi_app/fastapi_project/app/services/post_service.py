# app/services/post_service.py

from app.schemas.tables import Post
from app.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def create_post(self, title: str, content: str, user_id):
        post = Post(
            caption=title,
            user_id=user_id,
            image_url="someurl"
        )
        return self.repo.create(post)

    def get_posts(self):
        return self.repo.get_all()

    def get_post(self, post_id):
        return self.repo.get_by_id(post_id)

    def delete_post(self, post):
        return self.repo.delete(post)