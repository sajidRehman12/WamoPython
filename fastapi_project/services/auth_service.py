from fastapi import HTTPException, Depends ,Header
import datetime
from services.db_service import search_user
from services.token_service import createTokenForUser , verifyTokenForUser





def authenticate_user(username: str, password: str ):

    if search_user(username=username, password=password) is True:
        return createTokenForUser( {"username": username,
                                 "password": password} )
    else :
        return "user not authnticated"

   



def verifyReq(authorization:str = Header()):
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")
    user_name=verifyTokenForUser(authorization)
  
    print(user_name)
    for u in list:
        if u["name"]==user_name["username"]:
            return {"header": authorization}
    return "user not authorized"


