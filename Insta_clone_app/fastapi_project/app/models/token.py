
import uuid
from datetime import datetime ,timezone ,timedelta
from sqlalchemy import String, Text, DateTime, func ,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from sqlalchemy import CheckConstraint ,ForeignKey ,Boolean


class Token(Base):
    __tablename__ = "tokens"

    # Changed from UUID to plain Integer primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
