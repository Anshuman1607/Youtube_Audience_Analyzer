from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .core.cors import setup_cors
from .api.endpoints import router
from .core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="A full-stack application for analyzing YouTube audience data",
    version="1.0.0"
)

setup_cors(app)

app.include_router(router, prefix="/api/v1", tags=["analytics"])

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def root():
    return {"message": "YouTube Audience Analyzer API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
