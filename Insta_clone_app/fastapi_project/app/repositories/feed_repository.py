from app.models.tables import Like
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func ,or_,func
# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 
# from app.schemas.post import PostResponse
from app.models.tables import Post,User,Follow,Comment,Token,Notification,Like

from app.repositories.like_repository import LikeRepository
class FeedRepository:
    def __init__(self, db: Session ):
        self.db = db
        

    def get_feed(self, user_id: str, limit: int = 20, offset: int = 0):
        followed_users = (
        self.db.query(Follow.following_id)
        .filter(Follow.follower_id == user_id)
        .subquery()
    )
        posts = (
                self.db.query(
                    Post.id,
                    Post.caption,
                    Post.image_url,
                    User.username,
                    func.count(func.distinct(Like.id)).label("likes_count"),
                    func.count(func.distinct(Comment.id)).label("comments_count")


                )
                .join(User, User.id == Post.user_id)
                .outerjoin(Like, Like.post_id == Post.id)
                .outerjoin(Comment, Comment.post_id == Post.id)
                .filter(Post.is_published == True,
                    or_(
                        Post.user_id == user_id,
                        Post.user_id.in_(followed_users),
                    )
                ) .group_by(
                     Post.id,
                     User.username
                ).order_by(Post.published_at.desc())  

                .limit(limit).offset(offset)
                .all()
            )
        

        return posts
        