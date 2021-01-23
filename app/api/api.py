from fastapi import APIRouter

from app.core.config import settings

from .endpoints import login, users, wishlist

api_router = APIRouter(prefix=settings.api_v1_str)

api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(wishlist.router)
