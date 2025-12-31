from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.presentation.routes import router as web_router
from app.data.db import init_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/presentation/static"), name="static")
app.include_router(web_router)

@app.on_event("startup")
async def on_startup():
    await init_db()
