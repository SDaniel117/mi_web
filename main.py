from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.presentation.routes import router as web_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/presentation/static"), name="static")
app.include_router(web_router)