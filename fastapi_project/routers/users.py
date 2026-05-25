from fastapi import FastAPI ,Query, Depends , BackgroundTasks , APIRouter,Header , HTTPException
from models.user import User
from datetime import datetime
from jose import jwt
from typing import Annotated 
from models.login_model import LoginModel
from services.auth_service import authenticate_user
from services.user_service import create_user_service

router= APIRouter(prefix="/users",tags=["Users"])




@router.get("/")
def getUsers(id:int):
    return "users:list of users"



@router.post("/login")
def authentication(loginModel:LoginModel):
    return (authenticate_user(username=loginModel.name,password=loginModel.password))


@router.post("/user")
def create_user(user:User):
   return  create_user_service(user)

@router.get("/request")



# user authentication route


def userauthemail(name:str,mail:str):
    date = datetime.now()
    with open("log.txt", mode="a") as msgFile:
        content = f"notification for {name}: {mail} : {date} \n"
        msgFile.write(content)


# @router.post("/login")
# def login(user:User):
#     for u in list:
#         if u["name"] == user.name and u["password"] == user.password:
#             token = createTokenForUser({"username": u["name"]})
#             return {"access_token": token, "token_type": "bearer"}
#     return "user not found"



@router.get("/items")
def search_items(
    q: Annotated[str, Query(min_length=3, max_length=20)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 10
):
    return {
        "query": q,
        "page": page,
        "limit": limit
    }