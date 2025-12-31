from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.models import Piece

class PieceRepository:
    async def list_latest(self, db: AsyncSession, limit: int = 50) -> list[Piece]:
        q = select(Piece).order_by(desc(Piece.id)).limit(limit)
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
        title: str,
        description: str,
        tags: str,
        image_url: str,
        download_url: str,
    ) -> Piece:
        piece = Piece(
            title=title.strip(),
            description=description.strip(),
            tags=tags.strip(),
            image_url=image_url.strip(),
            download_url=download_url.strip(),
        )
        db.add(piece)
        await db.commit()
        await db.refresh(piece)
        return piece
