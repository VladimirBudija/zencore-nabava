from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    offer_number = Column(String, unique=True, index=True, nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    delivery_date = Column(DateTime)
    valid_until = Column(DateTime)
    notes = Column(Text)
    status = Column(String, default="active")  # active, expired, accepted, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    material = relationship("Material", back_populates="offers")
    vendor = relationship("Vendor", back_populates="offers")

    # Indeksi
    __table_args__ = (
        Index('idx_offer_number', 'offer_number'),
        Index('idx_offer_material', 'material_id'),
        Index('idx_offer_vendor', 'vendor_id'),
        Index('idx_offer_status', 'status'),
        Index('idx_offer_date', 'delivery_date'),
    ) 