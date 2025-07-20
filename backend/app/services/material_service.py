from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional
from ..models.material import Material
from ..models.receipt import Receipt
from ..models.consumption import Consumption
from ..schemas.material import MaterialWithCalculations


class MaterialService:
    
    @staticmethod
    def calculate_current_stock(db: Session, material_id: int) -> float:
        """Izračunava trenutnu zalihu materijala"""
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return 0.0
        
        # Suma prijema
        total_receipts = db.query(func.sum(Receipt.quantity)).filter(
            Receipt.material_id == material_id
        ).scalar() or 0.0
        
        # Suma utroška
        total_consumptions = db.query(func.sum(Consumption.quantity)).filter(
            Consumption.material_id == material_id
        ).scalar() or 0.0
        
        # Trenutna zaliha = početna zaliha + prijemi - utrošak
        current_stock = material.opening_stock + total_receipts - total_consumptions
        return max(0.0, current_stock)  # Ne može biti negativna
    
    @staticmethod
    def calculate_recommended_po(db: Session, material_id: int) -> float:
        """Izračunava preporučenu količinu za narudžbu"""
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return 0.0
        
        current_stock = MaterialService.calculate_current_stock(db, material_id)
        
        # Preporučena narudžba = sigurnosna zaliha + mjesečni forecast - trenutna zaliha
        recommended = material.safety_stock + material.monthly_forecast - current_stock
        
        # Dodaj 20% buffer za sigurnost
        recommended = recommended * 1.2
        
        return max(0.0, recommended)
    
    @staticmethod
    def get_stock_status(db: Session, material_id: int) -> str:
        """Određuje status zaliha (normal, low, critical)"""
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return "unknown"
        
        current_stock = MaterialService.calculate_current_stock(db, material_id)
        
        if current_stock <= material.safety_stock * 0.5:
            return "critical"
        elif current_stock <= material.safety_stock:
            return "low"
        else:
            return "normal"
    
    @staticmethod
    def get_last_activity_dates(db: Session, material_id: int) -> tuple[Optional[datetime], Optional[datetime]]:
        """Vraća datume zadnjeg prijema i utroška"""
        last_receipt = db.query(Receipt.receipt_date).filter(
            Receipt.material_id == material_id
        ).order_by(Receipt.receipt_date.desc()).first()
        
        last_consumption = db.query(Consumption.consumption_date).filter(
            Consumption.material_id == material_id
        ).order_by(Consumption.consumption_date.desc()).first()
        
        return (
            last_receipt[0] if last_receipt else None,
            last_consumption[0] if last_consumption else None
        )
    
    @staticmethod
    def get_material_with_calculations(db: Session, material_id: int) -> Optional[MaterialWithCalculations]:
        """Vraća materijal s kalkulacijama"""
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return None
        
        current_stock = MaterialService.calculate_current_stock(db, material_id)
        recommended_po = MaterialService.calculate_recommended_po(db, material_id)
        stock_status = MaterialService.get_stock_status(db, material_id)
        last_receipt_date, last_consumption_date = MaterialService.get_last_activity_dates(db, material_id)
        
        return MaterialWithCalculations(
            **material.__dict__,
            current_stock=current_stock,
            recommended_po=recommended_po,
            stock_status=stock_status,
            last_receipt_date=last_receipt_date,
            last_consumption_date=last_consumption_date
        )
    
    @staticmethod
    def get_low_stock_materials(db: Session) -> list[MaterialWithCalculations]:
        """Vraća materijale s niskim zalihama"""
        materials = db.query(Material).filter(Material.is_active == True).all()
        low_stock_materials = []
        
        for material in materials:
            material_with_calc = MaterialService.get_material_with_calculations(db, material.id)
            if material_with_calc and material_with_calc.stock_status in ["low", "critical"]:
                low_stock_materials.append(material_with_calc)
        
        return low_stock_materials 