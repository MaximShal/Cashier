from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class PaymentTypeEnum(str, Enum):
    cash = "cash"
    card = "card"


class PaymentCreate(BaseModel):
    type: PaymentTypeEnum
    amount: float


class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: float


class ProductResponse(ProductCreate):
    total: float

    class Config:
        from_attributes = True


class ReceiptBase(BaseModel):
    additional_data: Optional[str] = None
    payment: PaymentCreate


class ReceiptCreate(ReceiptBase):
    products: List[ProductCreate]


class ReceiptResponse(ReceiptBase):
    id: int
    products: List[ProductResponse]
    user_id: int
    total: float
    rest: float
    created_at: datetime

    class Config:
        from_attributes = True


class ReceiptList(BaseModel):
    receipts: List[ReceiptResponse]
