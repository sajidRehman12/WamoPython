import uuid
from datetime import datetime ,timezone ,timedelta
from sqlalchemy import String, Text, DateTime, func ,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from sqlalchemy import CheckConstraint ,ForeignKey ,Boolean
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
def _expires_at_default() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=24)


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True           )
    user_id: Mapped[int] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    media_url: Mapped[str] = mapped_column(String(500), nullable=False)
    media_type: Mapped[str] = mapped_column(String(10), nullable=False)  # "image" | "video"
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_expires_at_default, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    # RELATIONSHIPS ARE DEFINED BELOW
    author: Mapped["User"] = relationship("User", back_populates="stories")

