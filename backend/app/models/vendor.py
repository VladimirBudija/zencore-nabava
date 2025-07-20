from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    materials = relationship("Material", back_populates="vendor")
    offers = relationship("Offer", back_populates="vendor")
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
    receipts = relationship("Receipt", back_populates="vendor")

    # Indeksi
    __table_args__ = (
        Index('idx_vendor_code', 'code'),
        Index('idx_vendor_active', 'is_active'),
    ) 