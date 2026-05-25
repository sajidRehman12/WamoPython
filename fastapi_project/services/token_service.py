from jose import jwt

SECRET_KEY="this-is-my-secret-key-for-fastapi-app"
ALGORITHM = "HS256"


def createTokenForUser(userInformation:dict):
    data = userInformation.copy()
    return jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)

def verifyTokenForUser(token):
    return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
