from fastapi import FastAPI
from core.router import router as app_router
from core.config import settings
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(app_router)
