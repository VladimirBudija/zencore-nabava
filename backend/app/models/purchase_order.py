from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True, index=True, nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)
    expected_delivery = Column(DateTime)
    status = Column(String, default="pending")  # pending, confirmed, delivered, cancelled
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    material = relationship("Material", back_populates="purchase_orders")
    vendor = relationship("Vendor", back_populates="purchase_orders")
    user = relationship("User")
    receipts = relationship("Receipt", back_populates="purchase_order")

    # Indeksi
    __table_args__ = (
        Index('idx_po_number', 'po_number'),
        Index('idx_po_material', 'material_id'),
        Index('idx_po_vendor', 'vendor_id'),
        Index('idx_po_status', 'status'),
        Index('idx_po_date', 'order_date'),
    ) 