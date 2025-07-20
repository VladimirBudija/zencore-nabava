from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PurchaseOrderBase(BaseModel):
    po_number: str
    material_id: int
    vendor_id: int
    quantity: float
    unit_price: float
    total_amount: float
    order_date: datetime
    expected_delivery: Optional[datetime] = None
    notes: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    po_number: Optional[str] = None
    material_id: Optional[int] = None
    vendor_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    order_date: Optional[datetime] = None
    expected_delivery: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    status: str
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 