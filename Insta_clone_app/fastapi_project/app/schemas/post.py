# app/schemas/post_schema.py

from pydantic import BaseModel ,HttpUrl ,field_validator 
from typing import Optional
from datetime import datetime
import uuid


class PostCreate(BaseModel):
    title: str
    event_date:Optional[datetime]=None
    @field_validator('event_date')
    @classmethod
    def check_future(cls, v: datetime) -> datetime:
        if v <= datetime.now(v.tzinfo):
            raise ValueError('The date must be in the future.')
        return v
    class Config:
        from_attributes = True



class PostResponse(BaseModel):
    caption: str
    user_id: uuid.UUID
    image_url:HttpUrl
    class Config:
        from_attributes = True