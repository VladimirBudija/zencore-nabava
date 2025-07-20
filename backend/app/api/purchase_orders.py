from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.purchase_order import PurchaseOrder
from ..schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse

router = APIRouter(prefix="/purchase-orders", tags=["purchase_orders"])


@router.get("/", response_model=List[PurchaseOrderResponse])
async def get_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    purchase_orders = db.query(PurchaseOrder).offset(skip).limit(limit).all()
    return purchase_orders


@router.post("/", response_model=PurchaseOrderResponse)
async def create_purchase_order(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    existing_po = db.query(PurchaseOrder).filter(PurchaseOrder.po_number == purchase_order.po_number).first()
    if existing_po:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Purchase order with this number already exists"
        )
    
    db_po = PurchaseOrder(**purchase_order.dict(), created_by=current_user.id)
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    return db_po


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
async def get_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found"
        )
    return po


@router.put("/{po_id}", response_model=PurchaseOrderResponse)
async def update_purchase_order(
    po_id: int,
    purchase_order: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not db_po:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found"
        )
    
    update_data = purchase_order.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_po, field, value)
    
    db.commit()
    db.refresh(db_po)
    return db_po


@router.delete("/{po_id}")
async def delete_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not db_po:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase order not found"
        )
    
    db_po.status = "cancelled"
    db.commit()
    return {"message": "Purchase order cancelled successfully"} 