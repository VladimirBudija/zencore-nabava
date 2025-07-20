from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConsumptionBase(BaseModel):
    consumption_number: str
    material_id: int
    quantity: float
    consumption_date: datetime
    project: Optional[str] = None
    cost_center: Optional[str] = None
    notes: Optional[str] = None


class ConsumptionCreate(ConsumptionBase):
    pass


class ConsumptionUpdate(BaseModel):
    consumption_number: Optional[str] = None
    material_id: Optional[int] = None
    quantity: Optional[float] = None
    consumption_date: Optional[datetime] = None
    project: Optional[str] = None
    cost_center: Optional[str] = None
    notes: Optional[str] = None


class ConsumptionResponse(ConsumptionBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 