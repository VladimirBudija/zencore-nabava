from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReceiptBase(BaseModel):
    receipt_number: str
    material_id: int
    purchase_order_id: Optional[int] = None
    vendor_id: int
    quantity: float
    unit_price: float
    total_amount: float
    receipt_date: datetime
    batch_number: Optional[str] = None
    notes: Optional[str] = None


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    receipt_number: Optional[str] = None
    material_id: Optional[int] = None
    purchase_order_id: Optional[int] = None
    vendor_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    receipt_date: Optional[datetime] = None
    batch_number: Optional[str] = None
    notes: Optional[str] = None


class ReceiptResponse(ReceiptBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 