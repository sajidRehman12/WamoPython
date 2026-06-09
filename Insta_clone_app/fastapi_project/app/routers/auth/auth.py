from fastapi import APIRouter, HTTPException ,Request ,Header
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.database.database import get_db
from app.repositories.user_repository import UserRepository
from app.core.oauth import get_current_user
from app.models.tables import User

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
    loginRequest: LoginRequest,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = AuthService(repo)

    token = service.login_user(
        username=loginRequest.username,
        password=loginRequest.password
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
    current_user :User = Depends(get_current_user)
 ):
    
  return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "profile_photo":current_user.avatar_url
    }



@router.post("/logout")
def logout(authorization:str = Header(None),db: Session = Depends(get_db),
           current_user :User = Depends(get_current_user)
 ):
    repo = UserRepository(db)
    service = AuthService(repo)
    _,token=authorization.split()
    service.logout(token)
    return "successfully logged out"


