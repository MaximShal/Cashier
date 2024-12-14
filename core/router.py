from fastapi import APIRouter
from .api_routes import router as api_router


router = APIRouter()
router.include_router(api_router, prefix="/api")
