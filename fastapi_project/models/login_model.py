from pydantic import BaseModel


class LoginModel (BaseModel):
    name:str
    password:str


