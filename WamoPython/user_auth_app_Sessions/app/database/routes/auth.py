from fastapi import APIRouter, Depends,HTTPException, status, Response, Request
from typing import List
from app.database.dependencies import  get_active_user ,create_access_token
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm




import datetime
import os
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
import shutil
from app.database.mock_db import (
    MOCK_USERS_DB,
    create_user,
    get_user_by_email,
    get_user_by_username,
    verify_password,
)
from app.database.models.schemas import LoginRequest, SignupRequest, UserResponse
load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/")
def homeRouter():
    return(os.getenv("SECRET_KEY"))


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest):
    if get_user_by_username(body.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if get_user_by_email(body.email):
        raise HTTPException(status_code=400, detail="Email already taken")
    user = create_user(
        username=body.username,
        full_name=body.full_name,
        email=body.email,
        password=body.password,
    )
    return user



@router.post("/login",operation_id="some_specific_id_you_define")
def login(body: LoginRequest,request:Request):
    user = get_user_by_username(body.username)
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is invalid",
        )
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account blocked")
   
    request.session["user"] = body.username
    return {"response": "user logged in successfully"}


@router.post("/logout")
def logout(request: Request,current_user: dict = Depends(get_active_user)):
    current_user["is_active"]=False
    user=request.session["user"]
    
    request.session.clear

    return {f"{user} logged out successfully"}
   




@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_active_user)):
    return current_user

@router.get("/users", response_model=List[UserResponse])
def list_users(current_user: dict = Depends(get_active_user)):
    return MOCK_USERS_DB



@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    path = f"./{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return FileResponse(
        path=f"./{file.file}",
        filename="report.pdf",
        media_type="application/pdf"
    )