# from pydantic import BaseModel, EmailStr ,Field ,ConfigDict
# from datetime import datetime
# from typing import Optional



# class User(BaseModel):
#     username:str
#     email:EmailStr
#     hashed_password:str


# class  SignupRequest(BaseModel):
#     username: str = Field(
#         min_length=3,
#         max_length=30,
#         pattern=r"^[a-zA-Z0-9_]+$",
#         description="Only letters, numbers, underscore allowed"
#     )

#     email: EmailStr

#     password: str = Field(
#         min_length=8,
#         max_length=128,
#         description="Must be at least 8 characters"
#     )

#     first_name: str = Field(
#         default=None,
#         max_length=100
#     )

#     middle_name: Optional[str] = Field(
#         default=None,
#         max_length=100
#     )
#     last_name: str = Field(
#         default=None,
#         max_length=100
#     )



# class LoginRequest(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     username: str
#     password:str


# class  UserResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     username: str
#     email: EmailStr
#     full_name: Optional[str]
#     bio: Optional[str] = Field(default=None, max_length=250)
#     profile_pic_url: Optional[str]
#     is_active: bool
#     created_at: datetime

# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"


