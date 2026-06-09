# app/services/auth_service.py

from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token
from passlib.context import CryptContext
from app.database.mock_db import JWT_DB
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def login_user(self, username: str, password: str):
        user = self.repo.get_by_username(username)

        if not user:
            return None

        if not self.verify_password(password, user.password_hash):
            return None

        token = create_access_token(
            data={"user_id": str(user.id), "email": user.email}
        )
        JWT_DB.append({"token":token,
                       "status":"active"})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "email": user.email
        }
    

    def logout(self,token:str):
        for o in JWT_DB:
            if o["token"]==token:
                o["status"]="inactive"
        return "successfully logged out"
