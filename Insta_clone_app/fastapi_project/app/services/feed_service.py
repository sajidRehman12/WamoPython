







from app.repositories.feed_repository import FeedRepository

class FeedService:
    def __init__(self, repo:FeedRepository):
        self.repo = repo

    def get_feed(self, user_id: str, limit: int, offset: int):
        return self.repo.get_feed(user_id, limit, offset)