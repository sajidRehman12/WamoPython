from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


from fastapi import Depends
from fastapi import HTTPException

from jose import jwt
from jose import JWTError

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.oauth import oauth2_scheme
from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)
from app.repositories.user_repository import UserRepository
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    return user