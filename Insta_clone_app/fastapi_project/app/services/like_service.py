from uuid import UUID

from app.models.tables import Like
from app.services.notification_service import NotificationService
from app.repositories.like_repository import LikeRepository

class LikeService:

    def __init__(
        self,
        like_repo:LikeRepository,
        post_repo,
        notification_service: NotificationService
    ):
        self.like_repo = like_repo
        self.post_repo = post_repo
        self.notification_service = notification_service

    def like_post(
        self,
        post_id: int,
        user_id: int
    ):
        post = self.post_repo.get_by_id(post_id,user_id)

        if not post:
            raise ValueError("Post not found")

        existing_like = self.like_repo.get_user_like(
            user_id=user_id,
            post_id=post_id
        )

        if existing_like:
            raise ValueError("Already liked")

        like = Like(
            user_id=user_id,
            post_id=post_id
        )

        like = self.like_repo.create(like)

        if post.user_id != user_id:
            self.notification_service.create_notification(
                recipient_id=post.user_id,
                actor_id=user_id,
                notification_type="like",
                target_id=post.id,
                target_type="post"
            )

        return like

    def unlike_post(
        self,
        post_id: int,
        user_id: int
    ):
        like = self.like_repo.get_user_like(
            user_id=user_id,
            post_id=post_id
        )

        if not like:
            raise ValueError("Like not found")

        self.like_repo.delete(like)

        return {
            "message": "Post unliked successfully"
        }
    

    def likes_on_a_post(
        self,
        post_id: int,
    ):
        like = self.like_repo.get_likes_on_a_post(
            post_id=post_id
        )
        return like
        