from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.consumption import Consumption
from ..schemas.consumption import ConsumptionCreate, ConsumptionUpdate, ConsumptionResponse

router = APIRouter(prefix="/consumptions", tags=["consumptions"])


@router.get("/", response_model=List[ConsumptionResponse])
async def get_consumptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    consumptions = db.query(Consumption).offset(skip).limit(limit).all()
    return consumptions


@router.post("/", response_model=ConsumptionResponse)
async def create_consumption(
    consumption: ConsumptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    existing_consumption = db.query(Consumption).filter(
        Consumption.consumption_number == consumption.consumption_number
    ).first()
    if existing_consumption:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consumption with this number already exists"
        )
    
    db_consumption = Consumption(**consumption.dict(), created_by=current_user.id)
    db.add(db_consumption)
    db.commit()
    db.refresh(db_consumption)
    return db_consumption


@router.get("/{consumption_id}", response_model=ConsumptionResponse)
async def get_consumption(
    consumption_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    consumption = db.query(Consumption).filter(Consumption.id == consumption_id).first()
    if not consumption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumption not found"
        )
    return consumption


@router.put("/{consumption_id}", response_model=ConsumptionResponse)
async def update_consumption(
    consumption_id: int,
    consumption: ConsumptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_consumption = db.query(Consumption).filter(Consumption.id == consumption_id).first()
    if not db_consumption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumption not found"
        )
    
    update_data = consumption.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_consumption, field, value)
    
    db.commit()
    db.refresh(db_consumption)
    return db_consumption


@router.delete("/{consumption_id}")
async def delete_consumption(
    consumption_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_consumption = db.query(Consumption).filter(Consumption.id == consumption_id).first()
    if not db_consumption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumption not found"
        )
    
    db.delete(db_consumption)
    db.commit()
    return {"message": "Consumption deleted successfully"} 