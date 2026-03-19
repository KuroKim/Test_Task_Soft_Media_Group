from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(String, index=True)

    # `short_id` is the unique key for lookups
    short_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    clicks: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
