from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .models import Receipt, Product
from .schemas import ReceiptCreate, PaymentCreate


def create_receipt(db: Session, receipt_data: ReceiptCreate, user_id: int):
    receipt = Receipt(
        user_id=user_id,
        payment_type=receipt_data.payment.type,
        payment_amount=receipt_data.payment.amount,
        additional_data=receipt_data.additional_data,
        created_at=func.now(),
        total=0.0,
        rest=receipt_data.payment.amount
    )
    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    for product_data in receipt_data.products:
        product = Product(
            name=product_data.name,
            price=product_data.price,
            quantity=product_data.quantity,
            total=product_data.price * product_data.quantity,
            receipt_id=receipt.id
        )
        db.add(product)
    db.commit()

    total = round(sum(p.total for p in receipt.products), 2)
    receipt.total = total
    receipt.rest = receipt.payment_amount - total
    db.commit()

    receipt.payment = PaymentCreate(type=receipt.payment_type, amount=receipt.payment_amount)
    return receipt


def list_receipt(db: Session, user_id: int):
    receipts = db.query(Receipt).filter(Receipt.user_id == user_id).all()
    for receipt in receipts:
        receipt.payment = PaymentCreate(type=receipt.payment_type, amount=receipt.payment_amount)
    return {"receipts": receipts}


def retrieve_receipt(db: Session, receipt_id: int, user_id: int):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id, Receipt.user_id == user_id).first()
    receipt.payment = PaymentCreate(type=receipt.payment_type, amount=receipt.payment_amount)
    return receipt
