
class ReplyService:

    def __init__(
        self,
        comment_repo,
        reply_repo,
        notification_service
    ):
        self.comment_repo = comment_repo
        self.reply_repo = reply_repo
        self.notification_service = notification_service

    def create_reply(
        self,
        comment_id,
        user_id,
        content
    ):
        parent_comment = (
            self.comment_repo.get_by_id(comment_id)
        )

        if not parent_comment:
            raise ValueError("Comment not found")

        reply = self.reply_repo.create(
            comment_id=comment_id,
            user_id=user_id,
            content=content
        )

        if parent_comment.user_id != user_id:
            self.notification_service.create_notification(
                recipient_id=parent_comment.user_id,
                actor_id=user_id,
                notification_type="reply",
                target_id=reply.id,
                target_type="comment"
            )

        return reply