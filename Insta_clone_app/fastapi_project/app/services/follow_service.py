from uuid import UUID
from app.models.tables import Follow
from app.repositories.follow_repository import FollowRepository

class FollowService:

    def __init__(self, follow_repo : FollowRepository, notification_service):
        self.follow_repo = follow_repo
        self.notification_service = notification_service

    def follow_user(self, follower_id: int, following_id: int):

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
    def unfollow_user(self, follower_id: int, following_id: int):

        follow = self.follow_repo.get_follow(follower_id, following_id)

        if not follow:
            raise ValueError("Not following")

        self.follow_repo.delete(follow)

        return {"message": "Unfollowed"}
    
    def get_followers_list(self,user_id):
        return self.follow_repo.count_followers(user_id=user_id)
    
    def get_following_list(self,user_id):
        return self.follow_repo.count_following(user_id=user_id)

    def get_full_list_followers_list(self,user_id):
        return self.follow_repo.list_followers(user_id=user_id)
    
    def get_full_list_following_list(self,user_id):
        return self.follow_repo.list_following(user_id=user_id)
