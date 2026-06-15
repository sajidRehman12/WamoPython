# app/schemas/post_schema.py

from pydantic import BaseModel ,HttpUrl ,field_validator 
from typing import Optional
from datetime import datetime,timezone
import uuid


class PostCreate(BaseModel):
    title: str
    event_date:Optional[datetime]=None
   
    @field_validator('event_date')
    @classmethod
    def check_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is None:
            return v
            
        if v.tzinfo is not None:
            v = v.astimezone(timezone.utc)
            current_time = datetime.now(timezone.utc)
        else:
            current_time = datetime.now()

        if v <= current_time:
            raise ValueError('The date must be in the future.')
            
        return v
    class Config:
        from_attributes = True



class PostResponse(BaseModel):
    caption: str | None
    image_url: HttpUrl
    id:int
    username: str
    likes_count: int
    comments_count: int

    class Confif:
        from_attributes=True