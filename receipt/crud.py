from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from core.config import settings
from .models import Receipt, Product, PaymentType
from .schemas import ReceiptCreate, PaymentCreate, PaymentTypeEnum


def create_receipt(db: Session, receipt_data: ReceiptCreate, user_id: int) -> Receipt:
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
    receipt.link = f"{settings.DOMAIN}/api/receipt/view/{receipt.link_id}"
    return receipt


def list_receipt(
        db: Session,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_total: Optional[float] = None,
        payment_type: Optional[PaymentTypeEnum] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
) -> dict[str:type[Receipt]]:
    query = db.query(Receipt).filter(Receipt.user_id == user_id)

    if start_date:
        query = query.filter(Receipt.created_at >= start_date)
    if end_date:
        query = query.filter(Receipt.created_at <= end_date)
    if min_total:
        query = query.filter(Receipt.total >= min_total)
    if payment_type:
        query = query.filter(Receipt.payment_type == payment_type)

    receipts = query.offset(offset).limit(limit).all()
    for receipt in receipts:
        receipt.payment = PaymentCreate(type=receipt.payment_type, amount=receipt.payment_amount)
        receipt.link = f"{settings.DOMAIN}/api/receipt/view/{receipt.link_id}"
    return {"receipts": receipts}


def retrieve_receipt(db: Session, receipt_id: int, user_id: int) -> type[Receipt]:
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id, Receipt.user_id == user_id).first()
    receipt.payment = PaymentCreate(type=receipt.payment_type, amount=receipt.payment_amount)
    receipt.link = f"{settings.DOMAIN}/api/receipt/view/{receipt.link_id}"
    return receipt


def generate_receipt_text(receipt: type[Receipt], line_length: int = 32) -> str:
    header = settings.COMPANY_NAME.center(line_length)
    separator = "=" * line_length
    footer = "Дякуємо за покупку!".center(line_length)
    date_str = receipt.created_at.strftime("%d.%m.%Y %H:%M").center(line_length)

    product_lines = []
    products_len = len(receipt.products)
    for i, product in enumerate(receipt.products):
        quantity_price = f"{product.quantity:.2f} x {product.price:.2f}".ljust(line_length // 2)
        total_price = f"{product.total:.2f}".rjust(line_length // 2)
        product_lines.append(quantity_price + total_price)
        product_name = product.name

        while len(product_name) > line_length:
            product_lines.append(product_name[:line_length])
            product_name = product_name[line_length:]
        product_lines.append(product_name)
        if i != products_len - 1:
            product_lines.append("-" * line_length)

    total_line = f"СУМА".ljust(line_length // 2) + f"{receipt.total:.2f}".rjust(line_length // 2)
    if receipt.payment_type == PaymentType.cash:
        payment_type_str = "ГОТІВКА"
    else:
        payment_type_str = "КАРТКА"
    payment_line = (f"{payment_type_str.capitalize()}".ljust(line_length // 2)
                    + f"{receipt.payment_amount:.2f}".rjust(line_length // 2))
    rest_line = f"Решта".ljust(line_length // 2) + f"{receipt.rest:.2f}".rjust(line_length // 2)

    product_lines = '\n'.join(product_lines)
    receipt_text = (
        f"{header}\n"
        f"{separator}\n"
        f"{product_lines}\n"
        f"{separator}\n"
        f"{total_line}\n"
        f"{payment_line}\n"
        f"{rest_line}\n"
        f"{separator}\n"
        f"{date_str}\n"
        f"{footer}"
    )
    return receipt_text
