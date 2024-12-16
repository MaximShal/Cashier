from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING
from core.auth import get_current_user
from core.database import get_db
from . import crud, schemas

router = APIRouter()
if TYPE_CHECKING:
    from user.models import User


@router.post("", response_model=schemas.ReceiptResponse)
async def create_receipt_route(
        receipt_data: schemas.ReceiptCreate,
        db: Session = Depends(get_db),
        current_user: "User" = Depends(get_current_user)
):
    receipt = crud.create_receipt(db, receipt_data, current_user.id)
    return receipt


@router.get("", response_model=schemas.ReceiptList)
async def list_receipt_route(
        db: Session = Depends(get_db),
        current_user: "User" = Depends(get_current_user)
):
    receipts = crud.list_receipt(db, current_user.id)
    return receipts


@router.get("/{receipt_id}", response_model=schemas.ReceiptResponse)
async def retrieve_receipt_route(
        receipt_id: int,
        db: Session = Depends(get_db),
        current_user: "User" = Depends(get_current_user)
):
    receipt = crud.retrieve_receipt(db, receipt_id, current_user.id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt
