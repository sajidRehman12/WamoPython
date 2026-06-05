from fastapi import APIRouter, HTTPException
from app.models.auth import RegisterRequest, LoginRequest, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.database.database import get_db
from app.repositories.user_repository import UserRepository
from fastapi.security import OAuth2PasswordBearer
from app.core.oauth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(userRequest:RegisterRequest, db: Session = Depends(get_db)):

    service = UserService(db)

    try:
        user = service.register_user(userRequest.username,userRequest.email, userRequest.password)
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = AuthService(repo)

    token = service.login_user(
        username=form_data.username,
        password=form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_profile(
    current_user = Depends(get_current_user)
):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    }



