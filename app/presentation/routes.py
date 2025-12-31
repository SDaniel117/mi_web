from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import SessionLocal
from app.data.repositories import PieceRepository
from app.services.pieces_service import normalize_tags, is_valid_url
from app.services.auth_service import check_admin

router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")
security = HTTPBasic()
repo = PieceRepository()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if not check_admin(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="No autorizado", headers={"WWW-Authenticate": "Basic"})
    return True

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    pieces = await repo.list_latest(db)
    return templates.TemplateResponse("home.html", {"request": request, "pieces": pieces})

@router.get("/piezas/{piece_id}", response_class=HTMLResponse)
async def piece_detail(request: Request, piece_id: int, db: AsyncSession = Depends(get_db)):
    piece = await repo.get_by_id(db, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    return templates.TemplateResponse("piece_detail.html", {"request": request, "piece": piece})

@router.get("/admin", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_form(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "error": ""})

@router.post("/admin", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_create(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    image_url: str = Form(...),
    download_url: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    tags_norm = normalize_tags(tags)

    if not title.strip():
        return templates.TemplateResponse("admin.html", {"request": request, "error": "El título es obligatorio."})
    if not is_valid_url(image_url):
        return templates.TemplateResponse("admin.html", {"request": request, "error": "Image URL debe iniciar con http(s)."})
    if not is_valid_url(download_url):
        return templates.TemplateResponse("admin.html", {"request": request, "error": "Download URL debe iniciar con http(s)."})
    if "drive.google.com" in download_url.lower():
        # Nota rápida: funciona si el Drive está “Cualquiera con el enlace”
        pass

    piece = await repo.create(
        db,
        title=title,
        description=description,
        tags=tags_norm,
        image_url=image_url,
        download_url=download_url,
    )

    return RedirectResponse(url=f"/piezas/{piece.id}", status_code=303)

@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})
