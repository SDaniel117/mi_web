import os
import ssl
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

raw_url = (os.getenv("DATABASE_URL") or "").strip()

if not raw_url:
    DATABASE_URL = "sqlite+aiosqlite:///./catalogo.db"
    connect_args = {}
else:
    # Normaliza esquema para asyncpg
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql://", 1)
    if raw_url.startswith("postgresql://"):
        DATABASE_URL = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        DATABASE_URL = raw_url

    # Neon requiere TLS -> SSLContext
    ssl_context = ssl.create_default_context()
    connect_args = {"ssl": ssl_context}

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def init_db() -> None:
    from app.data.models import Catalog, Piece  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
