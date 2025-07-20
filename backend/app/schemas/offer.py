from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OfferBase(BaseModel):
    offer_number: str
    material_id: int
    vendor_id: int
    unit_price: float
    quantity: float
    delivery_date: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    notes: Optional[str] = None


class OfferCreate(OfferBase):
    pass


class OfferUpdate(BaseModel):
    offer_number: Optional[str] = None
    material_id: Optional[int] = None
    vendor_id: Optional[int] = None
    unit_price: Optional[float] = None
    quantity: Optional[float] = None
    delivery_date: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class OfferResponse(OfferBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 