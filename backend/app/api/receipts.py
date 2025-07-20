from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.receipt import Receipt
from ..schemas.receipt import ReceiptCreate, ReceiptUpdate, ReceiptResponse

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.get("/", response_model=List[ReceiptResponse])
async def get_receipts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    receipts = db.query(Receipt).offset(skip).limit(limit).all()
    return receipts


@router.post("/", response_model=ReceiptResponse)
async def create_receipt(
    receipt: ReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    existing_receipt = db.query(Receipt).filter(Receipt.receipt_number == receipt.receipt_number).first()
    if existing_receipt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Receipt with this number already exists"
        )
    
    db_receipt = Receipt(**receipt.dict(), created_by=current_user.id)
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt


@router.get("/{receipt_id}", response_model=ReceiptResponse)
async def get_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return receipt


@router.put("/{receipt_id}", response_model=ReceiptResponse)
async def update_receipt(
    receipt_id: int,
    receipt: ReceiptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    
    update_data = receipt.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_receipt, field, value)
    
    db.commit()
    db.refresh(db_receipt)
    return db_receipt


@router.delete("/{receipt_id}")
async def delete_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    
    db.delete(db_receipt)
    db.commit()
    return {"message": "Receipt deleted successfully"} 