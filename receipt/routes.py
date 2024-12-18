from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from typing import TYPE_CHECKING, Optional
from core.auth import get_current_user
from core.database import get_db
from . import crud, schemas
from .models import Receipt

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
        current_user: "User" = Depends(get_current_user),
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_total: Optional[float] = None,
        payment_type: Optional[schemas.PaymentTypeEnum] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
):
    current_date = datetime.utcnow().date()
    if start_date and end_date:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date cannot be later than end date.")
        if start_date.date() > current_date or end_date.date() > current_date:
            raise HTTPException(status_code=400, detail="Dates cannot be in the future.")
    return crud.list_receipt(db, current_user.id, start_date, end_date, min_total, payment_type, limit, offset)


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


@router.get("/view/{link_id}", response_class=PlainTextResponse)
async def view_receipt(
    link_id: str,
    db: Session = Depends(get_db),
    line_length: int = Query(32, ge=20, le=80, description="Receipt width")
):
    receipt = db.query(Receipt).filter(Receipt.link_id == link_id).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    receipt_text = crud.generate_receipt_text(receipt, line_length)
    return PlainTextResponse(receipt_text)
