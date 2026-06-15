from sqlalchemy.orm import Session,query
from sqlalchemy import select
from app.models.tables import User
from fastapi import HTTPException
from app.models.tables import Token
class TokenRepository:

    def __init__(self, db: Session):
        self.db = db
    def save_token(self,token:str,status:str="active"):
        token=Token(token=token,status=status)
        self.db.add(token)
        self.db.commit()
    def blacklist_user(self,token:str):
        tokenFromDb = self.db.query(Token).filter(Token.token==token).first()
        if tokenFromDb is not None:
            tokenFromDb.status="inactive"
            self.db.commit()
            return True
        else:
            return False