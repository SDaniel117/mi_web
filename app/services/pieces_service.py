from app.data.repositories import PieceRepository

repo = PieceRepository()

def normalize_tags(tags: str) -> str:
    # Limpia espacios y deja "tag1, tag2, tag3"
    parts = [t.strip() for t in (tags or "").split(",")]
    parts = [t for t in parts if t]
    return ", ".join(parts)

def is_valid_url(url: str) -> bool:
    u = (url or "").strip().lower()
    return u.startswith("http://") or u.startswith("https://")
