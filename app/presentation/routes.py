from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.home_service import get_home_message

router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    msg = get_home_message()
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "msg": msg}
    )

@router.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request):
    return templates.TemplateResponse(
        "privacy.html",
        {"request": request}
    )
