
from models.user import User
from database.user_data import list_of_users 


def create_user_service(user:User):
    id=list_of_users.__len__()+1
    names=[u["name"] for u in list_of_users]
    if user.name in names:
        return{ "response": "user already exists"}
    else:
        u ={"id": id,
            "name":user.name,
            "password":user.password } 
        list_of_users.append(u)
        return{ "response": "user created successfully"}