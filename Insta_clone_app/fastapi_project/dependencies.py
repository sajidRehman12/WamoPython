# # # dependencies.py

# # from fastapi import Depends, HTTPException, status ,Request
# # from datetime import datetime ,timedelta
# # from database.mock_db import get_user_by_username
# # from config import ACCESS_TOKEN_EXPIRE_MINUTES ,ALGORITHM ,SECRET_KEY
# # from jose import JWTError ,jwt


# # def create_access_token(data: dict) -> str:
# #     payload = data.copy()
# #     expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     payload.update({"exp": expire})
# #     return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# # def decode_access_token(token: str) -> dict:
# #     try:
# #         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #     except JWTError:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid or expired token",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )



# # def get_current_user(request:Request) -> dict:
# #     username: str = request.session["user"]

# #     if not username:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Token payload invalid",
# #         )

# #     user = get_user_by_username(username)
# #     if not user:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="User not found",
# #         )
# #     return user


# # def get_active_user(current_user: dict = Depends(get_current_user)) -> dict:
# #     if not current_user["is_active"]:
# #         raise HTTPException(
# #             status_code=status.HTTP_403_FORBIDDEN,
# #             detail="Inactive user account",
# #         )
# #     return current_user
# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta

# SECRET_KEY = "super-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str):
#     return password
#     # return pwd_context.hash(password)


# def verify_password(plain_password, hashed_password):
#     return True
#     return pwd_context.verify(plain_password, hashed_password)


# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})

#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
