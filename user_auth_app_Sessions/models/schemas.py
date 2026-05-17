# schemas.py
from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    is_active: bool
