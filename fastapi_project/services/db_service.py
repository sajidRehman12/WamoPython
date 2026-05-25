

from fastapi import Depends 
from database.user_data import list_of_users



def search_user(username: str, password: str):
    
    for u in list_of_users:
        if username == u["name"]:
            if password == u["password"]:
                return True
            else:
                return False
    return False
