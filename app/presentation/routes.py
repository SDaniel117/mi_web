from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import SessionLocal
from app.data.repositories import CatalogRepository, PieceRepository
from app.services.pieces_service import normalize_tags, is_valid_url
from app.services.auth_service import check_admin

router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")
security = HTTPBasic()

cat_repo = CatalogRepository()
piece_repo = PieceRepository()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if not check_admin(credentials.username, credentials.password):
        raise HTTPException(status_code=401, detail="No autorizado", headers={"WWW-Authenticate": "Basic"})
    return True

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    catalogs = await cat_repo.list_latest(db)
    return templates.TemplateResponse("home.html", {"request": request, "catalogs": catalogs})

@router.get("/catalogos/{catalog_id}", response_class=HTMLResponse)
async def catalog_detail(request: Request, catalog_id: int, db: AsyncSession = Depends(get_db)):
    catalog = await cat_repo.get_by_id(db, catalog_id)
    if not catalog:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    pieces = await piece_repo.list_by_catalog(db, catalog_id)
    return templates.TemplateResponse(
        "catalog_detail.html",
        {"request": request, "catalog": catalog, "pieces": pieces},
    )

@router.get("/piezas/{piece_id}", response_class=HTMLResponse)
async def piece_detail(request: Request, piece_id: int, db: AsyncSession = Depends(get_db)):
    piece = await piece_repo.get_by_id(db, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    return templates.TemplateResponse("piece_detail.html", {"request": request, "piece": piece})

# Admin: crear catálogo
@router.get("/admin/catalogos", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_catalog_form(request: Request):
    return templates.TemplateResponse("admin_catalog.html", {"request": request, "error": ""})

@router.post("/admin/catalogos", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_catalog_create(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    image_url: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    tags_norm = normalize_tags(tags)

    if not title.strip():
        return templates.TemplateResponse("admin_catalog.html", {"request": request, "error": "El título es obligatorio."})
    if not is_valid_url(image_url):
        return templates.TemplateResponse("admin_catalog.html", {"request": request, "error": "Image URL debe iniciar con http(s)."})
    catalog = await cat_repo.create(db, title=title, description=description, tags=tags_norm, image_url=image_url)
    return RedirectResponse(url=f"/catalogos/{catalog.id}", status_code=303)

# Admin: crear pieza dentro de un catálogo
@router.get("/admin/catalogos/{catalog_id}/piezas", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_piece_form(request: Request, catalog_id: int, db: AsyncSession = Depends(get_db)):
    catalog = await cat_repo.get_by_id(db, catalog_id)
    if not catalog:
        raise HTTPException(status_code=404, detail="Catálogo no encontrado")
    return templates.TemplateResponse("admin_piece.html", {"request": request, "error": "", "catalog": catalog})

@router.post("/admin/catalogos/{catalog_id}/piezas", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
async def admin_piece_create(
    request: Request,
    catalog_id: int,
    title: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""),
    image_url: str = Form(...),
    download_url: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    tags_norm = normalize_tags(tags)

    if not title.strip():
        return templates.TemplateResponse("admin_piece.html", {"request": request, "error": "El título es obligatorio.", "catalog": {"id": catalog_id}})
    if not is_valid_url(image_url):
        return templates.TemplateResponse("admin_piece.html", {"request": request, "error": "Image URL debe iniciar con http(s).", "catalog": {"id": catalog_id}})
    if not is_valid_url(download_url):
        return templates.TemplateResponse("admin_piece.html", {"request": request, "error": "Download URL debe iniciar con http(s).", "catalog": {"id": catalog_id}})

    piece = await piece_repo.create(
        db,
        catalog_id=catalog_id,
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
