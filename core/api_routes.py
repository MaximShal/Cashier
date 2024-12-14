from fastapi import APIRouter
from user.routes import router as users_router
from receipt.routes import router as receipt_router

router = APIRouter()
router.include_router(users_router, prefix="/user")
router.include_router(receipt_router, prefix="/receipt")
