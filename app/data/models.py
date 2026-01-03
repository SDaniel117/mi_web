from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.data.db import Base

class Catalog(Base):
    __tablename__ = "catalogs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(String(250), default="")
    image_url: Mapped[str] = mapped_column(String(600))
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    pieces: Mapped[list["Piece"]] = relationship(
        back_populates="catalog",
        cascade="all, delete-orphan",
    )

class Piece(Base):
    __tablename__ = "pieces"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    catalog_id: Mapped[int] = mapped_column(ForeignKey("catalogs.id"), index=True)

    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(String(250), default="")
    image_url: Mapped[str] = mapped_column(String(600))
    download_url: Mapped[str] = mapped_column(String(800))
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    catalog: Mapped["Catalog"] = relationship(back_populates="pieces")
