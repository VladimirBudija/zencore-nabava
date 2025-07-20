from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.material import Material
from ..models.receipt import Receipt
from ..models.consumption import Consumption
from ..models.purchase_order import PurchaseOrder
from ..services.material_service import MaterialService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Rekapitulacija - glavni dashboard podaci"""
    
    # Ukupan broj materijala i usluga
    total_materials = db.query(Material).filter(
        Material.is_active == True,
        Material.item_type == "materijal"
    ).count()
    
    total_services = db.query(Material).filter(
        Material.is_active == True,
        Material.item_type == "usluga"
    ).count()
    
    # Materijali s niskim zalihama (samo materijali, ne usluge)
    low_stock_materials = MaterialService.get_low_stock_materials(db)
    
    # Ukupan broj aktivnih narudžbi
    active_pos = db.query(PurchaseOrder).filter(PurchaseOrder.status == "pending").count()
    
    # Ukupan broj prijema u zadnjih 30 dana
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_receipts = db.query(Receipt).filter(Receipt.receipt_date >= thirty_days_ago).count()
    
    # Ukupan utrošak u zadnjih 30 dana
    recent_consumptions = db.query(Consumption).filter(Consumption.consumption_date >= thirty_days_ago).count()
    
    # Statistike po kategorijama
    category_stats = db.query(
        Material.category,
        func.count(Material.id).label('count')
    ).filter(
        Material.is_active == True
    ).group_by(
        Material.category
    ).all()
    
    # Materijali s COA
    materials_with_coa = db.query(Material).filter(
        Material.is_active == True,
        Material.has_coa == True
    ).count()
    
    return {
        "total_materials": total_materials,
        "total_services": total_services,
        "total_items": total_materials + total_services,
        "low_stock_materials_count": len(low_stock_materials),
        "active_purchase_orders": active_pos,
        "recent_receipts_30d": recent_receipts,
        "recent_consumptions_30d": recent_consumptions,
        "materials_with_coa": materials_with_coa,
        "category_distribution": [
            {"category": item.category, "count": item.count}
            for item in category_stats
        ],
        "low_stock_materials": [
            {
                "id": m.id,
                "code": m.code,
                "name": m.name,
                "current_stock": m.current_stock,
                "safety_stock": m.safety_stock,
                "stock_status": m.stock_status
            }
            for m in low_stock_materials
        ]
    }


@router.get("/stock-status")
async def get_stock_status_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Pregled statusa zaliha po kategorijama"""
    
    materials = db.query(Material).filter(Material.is_active == True).all()
    
    status_counts = {"normal": 0, "low": 0, "critical": 0}
    category_counts = {}
    
    for material in materials:
        status = MaterialService.get_stock_status(db, material.id)
        status_counts[status] += 1
        
        category = material.category or "uncategorized"
        if category not in category_counts:
            category_counts[category] = {"normal": 0, "low": 0, "critical": 0}
        category_counts[category][status] += 1
    
    return {
        "overall_status": status_counts,
        "by_category": category_counts
    }


@router.get("/trends")
async def get_consumption_trends(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Trend utroška u zadnjih N dana"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Dnevni utrošak
    daily_consumption = db.query(
        func.date(Consumption.consumption_date).label('date'),
        func.sum(Consumption.quantity).label('total_quantity')
    ).filter(
        Consumption.consumption_date >= start_date
    ).group_by(
        func.date(Consumption.consumption_date)
    ).order_by(
        func.date(Consumption.consumption_date)
    ).all()
    
    # Dnevni prijemi
    daily_receipts = db.query(
        func.date(Receipt.receipt_date).label('date'),
        func.sum(Receipt.quantity).label('total_quantity')
    ).filter(
        Receipt.receipt_date >= start_date
    ).group_by(
        func.date(Receipt.receipt_date)
    ).order_by(
        func.date(Receipt.receipt_date)
    ).all()
    
    return {
        "consumption_trend": [
            {"date": str(item.date), "quantity": float(item.total_quantity)}
            for item in daily_consumption
        ],
        "receipts_trend": [
            {"date": str(item.date), "quantity": float(item.total_quantity)}
            for item in daily_receipts
        ]
    }


@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Preporučene akcije"""
    
    materials = db.query(Material).filter(Material.is_active == True).all()
    recommendations = []
    
    for material in materials:
        current_stock = MaterialService.calculate_current_stock(db, material.id)
        recommended_po = MaterialService.calculate_recommended_po(db, material.id)
        stock_status = MaterialService.get_stock_status(db, material.id)
        
        if stock_status in ["low", "critical"] and recommended_po > 0:
            recommendations.append({
                "material_id": material.id,
                "material_code": material.code,
                "material_name": material.name,
                "current_stock": current_stock,
                "safety_stock": material.safety_stock,
                "recommended_po": recommended_po,
                "priority": "high" if stock_status == "critical" else "medium"
            })
    
    # Sortiraj po prioritetu
    recommendations.sort(key=lambda x: 0 if x["priority"] == "high" else 1)
    
    return {
        "recommendations": recommendations,
        "total_recommendations": len(recommendations)
    } 