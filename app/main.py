from fastapi import FastAPI
from app.core.config import settings
from app.api.api import api_router

app = FastAPI(
    title="URL Shortener API",
    description="A simple and fast URL shortener service.",
    version="1.0.0"
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to URL Shortener API! Visit /docs for documentation."}
