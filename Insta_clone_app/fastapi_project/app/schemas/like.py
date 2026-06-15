from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class LikeWithUsername(BaseModel):
    id: int
    post_id: int
    created_at: datetime
    username: str  

    class Config:
        from_attributes = True