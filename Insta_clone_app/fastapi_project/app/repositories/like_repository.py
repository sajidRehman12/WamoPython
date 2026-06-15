from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tables import Like

from app.models.tables import Post

class LikeRepository():

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, like: Like):
        self.db.add(like)
        self.db.commit()
        self.db.refresh(like)
        return like
    
    def get_user_like(self,user_id:UUID,
            post_id:UUID):
        
        return self.db.query(Like).filter(Like.post_id==post_id,
                                        Like.user_id==user_id).first()
         
    def delete(self,like:Like):
        self.db.delete(like)
        self.db.commit()