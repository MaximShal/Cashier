from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.auth import create_access_token, get_current_user
from core.database import get_db
from . import crud, schemas
from .models import User

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(user_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_data.login, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(get_current_user)):
    return schemas.UserResponse.from_orm(current_user)


@router.post("", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == user_data.login).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this login already exists."
        )
    new_user = crud.create_user(db, login=user_data.login, password=user_data.password, name=user_data.name)
    return schemas.UserResponse.from_orm(new_user)
