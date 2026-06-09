from fastapi.security import OAuth2PasswordBearer 
from fastapi import Depends, HTTPException, Header

from app.database.mock_db import JWT_DB
from fastapi import Depends
from fastapi import HTTPException
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)
from app.repositories.user_repository import UserRepository
def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    
    logged_out_exception = HTTPException(
        status_code=401,
        detail="you are not logged in"
    )

    scheme,token=authorization.split()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        for o in JWT_DB:
            if o["token"]==authorization:
                if(o["status"]!="active"):
                    raise logged_out_exception
    except:
        raise logged_out_exception

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    return user