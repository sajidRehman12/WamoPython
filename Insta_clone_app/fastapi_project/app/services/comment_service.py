from uuid import UUID
from app.models.tables import Comment
from app.repositories.post_repository import PostRepository
class CommentService:

    def __init__(
        self,
        comment_repo,
        post_repo,
        notification_service
    ):
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.notification_service = notification_service

    def create_comment(
        self,
        post_id: int,
        user_id: int,
        body: str,
        parent_id: int | None = None
    ):
        post = self.post_repo.get_by_id(post_id,user_id)

        if not post:
            raise ValueError("Post not found")

        comment = Comment(
            post_id=post_id,
            user_id=user_id,
            body=body,
            parent_id=parent_id
        )

        comment = self.comment_repo.create(comment)


        if parent_id is None and post.user_id != user_id:
            self.notification_service.create_notification(
                recipient_id=post.user_id,
                actor_id=user_id,
                notification_type="comment",
                target_id=comment.id,
                target_type="comment"
            )

        if parent_id:
            parent_comment = self.comment_repo.get_by_id(parent_id)

            if parent_comment and parent_comment.user_id != user_id:
                self.notification_service.create_notification(
                    recipient_id=parent_comment.user_id,
                    actor_id=user_id,
                    notification_type="reply",
                    target_id=comment.id,
                    target_type="comment"
                )

        return comment

    def delete_comment(self, comment_id: int, user_id: int):

        comment = self.comment_repo.get_by_id(comment_id)

        if not comment:
            raise ValueError("Comment not found")

        if comment.user_id != user_id:
            raise PermissionError("Not allowed to delete this comment")

        self.comment_repo.delete(comment)

        return {"message": "Comment deleted successfully"}