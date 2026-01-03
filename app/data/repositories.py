from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.models import Catalog, Piece

class CatalogRepository:
    async def list_latest(self, db: AsyncSession, limit: int = 50) -> list[Catalog]:
        q = select(Catalog).order_by(desc(Catalog.id)).limit(limit)
        res = await db.execute(q)
        return list(res.scalars().all())

    async def get_by_id(self, db: AsyncSession, catalog_id: int) -> Catalog | None:
        q = select(Catalog).where(Catalog.id == catalog_id)
        res = await db.execute(q)
        return res.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        *,
        title: str,
        description: str,
        tags: str,
        image_url: str,
    ) -> Catalog:
        obj = Catalog(
            title=title.strip(),
            description=description.strip(),
            tags=tags.strip(),
            image_url=image_url.strip(),
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

class PieceRepository:
    async def list_by_catalog(self, db: AsyncSession, catalog_id: int, limit: int = 200) -> list[Piece]:
        q = select(Piece).where(Piece.catalog_id == catalog_id).order_by(desc(Piece.id)).limit(limit)
        res = await db.execute(q)
        return list(res.scalars().all())

    async def get_by_id(self, db: AsyncSession, piece_id: int) -> Piece | None:
        q = select(Piece).where(Piece.id == piece_id)
        res = await db.execute(q)
        return res.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        *,
        catalog_id: int,
        title: str,
        description: str,
        tags: str,
        image_url: str,
        download_url: str,
    ) -> Piece:
        obj = Piece(
            catalog_id=catalog_id,
            title=title.strip(),
            description=description.strip(),
            tags=tags.strip(),
            image_url=image_url.strip(),
            download_url=download_url.strip(),
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
