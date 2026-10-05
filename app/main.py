from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router

app = FastAPI(
    title="ComicCraft AI",
    description="AI Comic Story Creator",
    version="1.0.0"
)

app.include_router(router)

app.mount(
    "/images",
    StaticFiles(directory="generated_images"),
    name="images"
)