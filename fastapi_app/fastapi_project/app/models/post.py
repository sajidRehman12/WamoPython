# app/schemas/post_schema.py

from pydantic import BaseModel
import uuid


class PostCreate(BaseModel):
    title: str
    content: str
    
    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    id: uuid.UUID
    caption: str
    user_id: uuid.UUID

    class Config:
        from_attributes = True