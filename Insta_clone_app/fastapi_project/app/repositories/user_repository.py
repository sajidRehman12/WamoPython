from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.tables import User
# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 
from fastapi import HTTPException
class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: str):
        # return self.db.get(User, user_id)
        stmt = select(User).where(User.id == user_id)
        return self.db.scalars(stmt).first()
    def get_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        return self.db.scalars(stmt).first()

    def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def get_all(self):
        stmt = select(User)
        return self.db.scalars(stmt).all()

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()

    def update_user(self, user: User, data: dict):
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def save_profile_picture(self,user_id,image_url):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.avatar_url = image_url
        self.db.commit()
        self.db.refresh(user)
        return user


    