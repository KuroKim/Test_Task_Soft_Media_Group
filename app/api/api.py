from fastapi import APIRouter
from app.api.v1.endpoints import url

api_router = APIRouter()

# Мы не делаем префикс для редиректа, чтобы ссылка была максимально короткой (например, http://localhost:8000/aB3x9Q)
api_router.include_router(url.router, tags=["URLs"])
