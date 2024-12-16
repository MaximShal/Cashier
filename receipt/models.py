import enum
import uuid
from sqlalchemy import Column, Integer, String, Enum, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class PaymentType(enum.Enum):
    cash = "cash"
    card = "card"


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    additional_data = Column(Text, nullable=True)
    user = relationship("User", back_populates="receipts")
    products = relationship("Product", back_populates="receipt")
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_amount = Column(NUMERIC(10, 2), nullable=False)
    total = Column(NUMERIC(10, 2), nullable=False)
    rest = Column(NUMERIC(10, 2), nullable=False)
    link_id = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=True)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    total = Column(NUMERIC(10, 2), nullable=False)
    receipt_id = Column(Integer, ForeignKey('receipts.id'))
    receipt = relationship("Receipt", back_populates="products")
