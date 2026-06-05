from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.tables import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: str):
        return self.db.get(User, user_id)

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