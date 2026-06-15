from uuid import UUID

from sqlalchemy.orm import Session ,joinedload
from sqlalchemy import func
from app.models.tables import User
from app.models.tables import Like
# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 
# from app.models.tables import Post

class LikeRepository():

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, like: Like):
        self.db.add(like)
        self.db.commit()
        self.db.refresh(like)
        return like
    
    def get_like_count(self,post_id:int):
        return self.db.query(func.count(Like.id)).filter(Like.post_id==post_id).scalar()

    def get_user_like(self,user_id:int,
            post_id:int):
        
        return self.db.query(Like).filter(Like.post_id==post_id,
                                        Like.user_id==user_id).first()
         

    def get_likes_on_a_post(self,
            post_id:int):
        likes= self.db.query(Like.post_id,Like.created_at,User.username).join(User,User.id==Like.user_id).filter(Like.post_id==post_id).all()
        print(likes)
        return [
        {
            "post_id": row.post_id, 
            "created_at": row.created_at, 
            "username": row.username
        } 
        for row in likes
    ]

    
    def delete(self,like:Like):
        self.db.delete(like)
        self.db.commit()