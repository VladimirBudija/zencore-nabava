from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_number = Column(String, unique=True, index=True, nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    receipt_date = Column(DateTime, nullable=False)
    batch_number = Column(String)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    material = relationship("Material", back_populates="receipts")
    purchase_order = relationship("PurchaseOrder", back_populates="receipts")
    vendor = relationship("Vendor", back_populates="receipts")
    user = relationship("User")

    # Indeksi
    __table_args__ = (
        Index('idx_receipt_number', 'receipt_number'),
        Index('idx_receipt_material', 'material_id'),
        Index('idx_receipt_po', 'purchase_order_id'),
        Index('idx_receipt_vendor', 'vendor_id'),
        Index('idx_receipt_date', 'receipt_date'),
    ) 