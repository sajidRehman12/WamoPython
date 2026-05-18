from fastapi import APIRouter
from app.models.models import User

router=APIRouter( prefix="/users",
    tags=["Users"])



@router.get("/")
def home():
    return {"response":"this is home route for users"}


@router.post("/signup")
def signup(user:User):
    username=user.name
    password=user.password
    email=user.email
    print(username,password,email)
    return {"username:",username,
           "password:",password,
           "email:",email }
