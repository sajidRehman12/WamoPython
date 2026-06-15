from uuid import UUID

from app.models.tables import Follow


class FollowService:

    def __init__(self, follow_repo, notification_service):
        self.follow_repo = follow_repo
        self.notification_service = notification_service

    def follow_user(self, follower_id: UUID, following_id: UUID):

        if follower_id == following_id:
            raise ValueError("Cannot follow yourself")

        existing = self.follow_repo.get_follow(follower_id, following_id)
        if existing:
            raise ValueError("Already following")

        follow = Follow(
            follower_id=follower_id,
            following_id=following_id
        )

        follow = self.follow_repo.create(follow)

        self.notification_service.create_notification(
            recipient_id=following_id,
            actor_id=follower_id,
            notification_type="follow"
        )

        return follow

    def unfollow_user(self, follower_id: UUID, following_id: UUID):

        follow = self.follow_repo.get_follow(follower_id, following_id)

        if not follow:
            raise ValueError("Not following")

        self.follow_repo.delete(follow)

        return {"message": "Unfollowed"}