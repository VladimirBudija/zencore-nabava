from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Consumption(Base):
    __tablename__ = "consumptions"

    id = Column(Integer, primary_key=True, index=True)
    consumption_number = Column(String, unique=True, index=True, nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    consumption_date = Column(DateTime, nullable=False)
    project = Column(String)  # Projekt/radni nalog
    cost_center = Column(String)  # Centar troškova
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    material = relationship("Material", back_populates="consumptions")
    user = relationship("User")

    # Indeksi
    __table_args__ = (
        Index('idx_consumption_number', 'consumption_number'),
        Index('idx_consumption_material', 'material_id'),
        Index('idx_consumption_date', 'consumption_date'),
        Index('idx_consumption_project', 'project'),
    ) 