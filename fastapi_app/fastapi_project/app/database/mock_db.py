# mock_db.py
from passlib.context import CryptContext
from app.models.user import SignupRequest
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Mock user database with Pakistani names
MOCK_USERS_DB: list[dict] = [
    {
        "id": 1,
        "username": "ali_raza",
        "full_name": "Ali Raza",
        "email": "ali.raza@gmail.com",
        "hashed_password": pwd_context.hash("ali123"),
        "is_active": True,
    },
    {
        "id": 2,
        "username": "fatima_khan",
        "full_name": "Fatima Khan",
        "email": "fatima.khan@gmail.com",
        "hashed_password": pwd_context.hash("fatima123"),
        "is_active": True,
    },
    {
        "id": 3,
        "username": "usman_tariq",
        "full_name": "Usman Tariq",
        "email": "usman.tariq@gmail.com",
        "hashed_password": pwd_context.hash("usman123"),
        "is_active": False,
    },
]


SESSION_IDS={}


def get_user_by_username(username: str) -> dict | None:
    for user in MOCK_USERS_DB:
        if user["username"] == username:
            return user
    return None


def get_user_by_email(email: str) -> dict | None:
    for user in MOCK_USERS_DB:
        if user["email"] == email:
            return user
    return None


def create_user(user: SignupRequest) -> dict:
    
    new_user = {
        "id": len(MOCK_USERS_DB) + 1,
        "username": user.username,
        "full_name": user.first_name + user.middle_name + user.last_name,
        "email": user.email,
        "hashed_password": pwd_context.hash(user.password),
        "is_active": True,
    }
    MOCK_USERS_DB.append(new_user)
    return new_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

