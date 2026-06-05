
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str):
#     return pwd_context.hash(password)


# def verify_password(plain: str, hashed: str):
#     return pwd_context.verify(plain, hashed)# app/utils.py

# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str):
#     return pwd_context.hash(password)


# def verify_password(plain: str, hashed: str):
#     return pwd_context.verify(plain, hashed)

# from app.core.security import hash_password, verify_password, create_access_token
# from app.models.user import User

# # 🧠 fake DB (replace with real DB later)
# fake_users_db = {}


# def register_user(username: str, email: str, password: str):

#     if username in fake_users_db:
#         raise Exception("User already exists")

#     user = User(
#         username=username,
#         email=email,
#         hashed_password=hash_password(password),
#     )

#     fake_users_db[username] = user
#     return user


# def authenticate_user(username: str, password: str):

#     user = fake_users_db.get(username)

#     if not user:
#         return None

#     if not verify_password(password, user.hashed_password):
#         return None

#     return user


# def login_user(username: str, password: str):

#     user = authenticate_user(username, password)

#     if not user:
#         raise Exception("Invalid credentials")

#     token = create_access_token(
#         data={"sub": user.username}
#     )

#     return token


# def get_user(username: str):
#     return fake_users_db.get(username)


from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password


class UserService:

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, username: str, email: str, password: str):

        if self.repo.get_by_username(username):
            raise Exception("Username already exists")

        if self.repo.get_by_email(email):
            raise Exception("Email already exists")

        from app.schemas.tables import User

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )

        return self.repo.create_user(user)

    def authenticate_user(self, username: str, password: str):

        user = self.repo.get_by_username(username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def get_user_by_id(self, user_id: str):
        return self.repo.get_by_id(user_id)

    def get_all_users(self):
        return self.repo.get_all()

    def delete_user(self, user_id: str):

        user = self.repo.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        self.repo.delete_user(user)
        return {"message": "User deleted successfully"}

    def update_user(self, user_id: str, data: dict):

        user = self.repo.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        return self.repo.update_user(user, data)