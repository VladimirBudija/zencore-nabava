from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.offer import Offer
from ..schemas.offer import OfferCreate, OfferUpdate, OfferResponse

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("/", response_model=List[OfferResponse])
async def get_offers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    offers = db.query(Offer).offset(skip).limit(limit).all()
    return offers


@router.post("/", response_model=OfferResponse)
async def create_offer(
    offer: OfferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    existing_offer = db.query(Offer).filter(Offer.offer_number == offer.offer_number).first()
    if existing_offer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offer with this number already exists"
        )
    
    db_offer = Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


@router.get("/{offer_id}", response_model=OfferResponse)
async def get_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    return offer


@router.put("/{offer_id}", response_model=OfferResponse)
async def update_offer(
    offer_id: int,
    offer: OfferUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not db_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    update_data = offer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_offer, field, value)
    
    db.commit()
    db.refresh(db_offer)
    return db_offer


@router.delete("/{offer_id}")
async def delete_offer(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not db_offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    db.delete(db_offer)
    db.commit()
    return {"message": "Offer deleted successfully"} 