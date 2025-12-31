from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.data.db import Base

class Piece(Base):
    __tablename__ = "pieces"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(String(250), default="")
    image_url: Mapped[str] = mapped_column(String(600))
    download_url: Mapped[str] = mapped_column(String(800))
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
