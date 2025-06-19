from fastapi import APIRouter
from app.api.routes import plate

api_router = APIRouter()

api_router.include_router(plate.router)
