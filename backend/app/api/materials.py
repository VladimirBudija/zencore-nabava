from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.user import User
from ..models.material import Material
from ..schemas.material import MaterialCreate, MaterialUpdate, MaterialResponse, MaterialWithCalculations
from ..services.material_service import MaterialService

router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/", response_model=List[MaterialResponse])
async def get_materials(
    skip: int = 0,
    limit: int = 100,
    item_type: str = None,
    category: str = None,
    vendor_id: int = None,
    has_coa: bool = None,
    regulatory_status: str = None,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Material)
    
    # Filtriranje po tipu stavke
    if item_type:
        query = query.filter(Material.item_type == item_type)
    
    # Filtriranje po kategoriji
    if category:
        query = query.filter(Material.category == category)
    
    # Filtriranje po dobavljaču
    if vendor_id:
        query = query.filter(Material.vendor_id == vendor_id)
    
    # Filtriranje po COA
    if has_coa is not None:
        query = query.filter(Material.has_coa == has_coa)
    
    # Filtriranje po regulatornom statusu
    if regulatory_status:
        query = query.filter(Material.regulatory_status == regulatory_status)
    
    # Pretraživanje po nazivu, kodu ili opisu
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Material.name.ilike(search_filter)) |
            (Material.code.ilike(search_filter)) |
            (Material.description.ilike(search_filter)) |
            (Material.material_component.ilike(search_filter)) |
            (Material.service_description.ilike(search_filter))
        )
    
    # Samo aktivni materijali
    query = query.filter(Material.is_active == True)
    
    materials = query.offset(skip).limit(limit).all()
    return materials


@router.post("/", response_model=MaterialResponse)
async def create_material(
    material: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Provjeri postoji li materijal s istim kodom
    existing_material = db.query(Material).filter(Material.code == material.code).first()
    if existing_material:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Material with this code already exists"
        )
    
    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@router.get("/{material_id}", response_model=MaterialWithCalculations)
async def get_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    material_with_calc = MaterialService.get_material_with_calculations(db, material_id)
    if not material_with_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material_with_calc


@router.put("/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: int,
    material: MaterialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    
    # Provjeri kod ako se mijenja
    if material.code and material.code != db_material.code:
        existing_material = db.query(Material).filter(Material.code == material.code).first()
        if existing_material:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Material with this code already exists"
            )
    
    # Ažuriraj polja
    update_data = material.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_material, field, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material


@router.delete("/{material_id}")
async def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    
    # Soft delete - samo deaktiviraj
    db_material.is_active = False
    db.commit()
    return {"message": "Material deactivated successfully"}


@router.get("/{material_id}/current-stock")
async def get_material_current_stock(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    current_stock = MaterialService.calculate_current_stock(db, material_id)
    return {"material_id": material_id, "current_stock": current_stock}


@router.get("/{material_id}/recommended-po")
async def get_material_recommended_po(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recommended_po = MaterialService.calculate_recommended_po(db, material_id)
    return {"material_id": material_id, "recommended_po": recommended_po}


@router.get("/statistics/summary")
async def get_materials_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Dohvati statistike materijala i usluga"""
    total_materials = db.query(Material).filter(
        Material.is_active == True,
        Material.item_type == "materijal"
    ).count()
    
    total_services = db.query(Material).filter(
        Material.is_active == True,
        Material.item_type == "usluga"
    ).count()
    
    materials_with_coa = db.query(Material).filter(
        Material.is_active == True,
        Material.has_coa == True
    ).count()
    
    critical_stock_materials = db.query(Material).filter(
        Material.is_active == True,
        Material.item_type == "materijal"
    ).all()
    
    critical_count = 0
    for material in critical_stock_materials:
        current_stock = MaterialService.calculate_current_stock(db, material.id)
        if current_stock <= material.safety_stock * 0.5:
            critical_count += 1
    
    return {
        "total_materials": total_materials,
        "total_services": total_services,
        "materials_with_coa": materials_with_coa,
        "critical_stock_count": critical_count,
        "total_items": total_materials + total_services
    }


@router.get("/categories/{category}/items")
async def get_items_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Dohvati sve stavke po kategoriji"""
    items = db.query(Material).filter(
        Material.category == category,
        Material.is_active == True
    ).offset(skip).limit(limit).all()
    return items


@router.get("/vendors/{vendor_id}/items")
async def get_items_by_vendor(
    vendor_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Dohvati sve stavke po dobavljaču"""
    items = db.query(Material).filter(
        Material.vendor_id == vendor_id,
        Material.is_active == True
    ).offset(skip).limit(limit).all()
    return items


@router.get("/regulatory/{status}/items")
async def get_items_by_regulatory_status(
    status: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Dohvati sve stavke po regulatornom statusu"""
    items = db.query(Material).filter(
        Material.regulatory_status == status,
        Material.is_active == True
    ).offset(skip).limit(limit).all()
    return items 