from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from enum import Enum


class ItemType(str, Enum):
    MATERIAL = "materijal"
    SERVICE = "usluga"


class Category(str, Enum):
    ADAPTOGEN = "adaptogen"
    NOOTROPIC = "nootropik"
    VITAMIN = "vitamin"
    MINERAL = "mineral"
    PHOSPHOLIPID = "fosfolipid"
    AROMA = "aroma"
    AUXILIARY = "pomoćna_tvar"
    PRODUCTION = "proizvodnja"
    PACKAGING = "pakiranje"
    TRANSPORT = "prijevoz"
    STORAGE = "skladištenje"
    MARKETING = "marketing"
    OTHER = "ostalo"


class Form(str, Enum):
    POWDER = "prašak"
    CAPSULE = "kapsula"
    OIL = "ulje"
    EXTRACT = "ekstrakt"
    LIPOSOME = "liposom"
    MICROENCAPSULATED = "mikroenkapsula"
    TABLET = "tableta"
    LIQUID = "tekućina"
    OTHER = "ostalo"


class RegulatoryStatus(str, Enum):
    NOVEL_FOOD = "novel_food"
    FOOD_SUPPLEMENT = "dodatak_prehrani"
    SCHOOL_BAN = "školska_zabrana"
    APPROVED = "odobreno"
    PENDING = "na_čekanju"
    NOT_APPLICABLE = "nije_primjenjivo"


class MaterialBase(BaseModel):
    code: str
    name: str
    
    # Tip stavke
    item_type: ItemType = ItemType.MATERIAL
    
    # Materijal / Sastojak (za materijale)
    material_component: Optional[str] = None
    
    # Opis usluge
    service_description: Optional[str] = None
    
    # Kategorija
    category: Category
    
    # Oblik
    form: Optional[Form] = None
    
    # Standardizacija / Specifikacija
    standardization: Optional[str] = None
    
    # Doza po jedinici
    dose_per_unit: Optional[float] = None
    dose_unit: Optional[str] = None
    
    # Ukupna potrošnja / obujam
    total_consumption: Optional[float] = None
    consumption_unit: Optional[str] = None
    
    # Osnovne informacije
    description: Optional[str] = None
    unit: str
    opening_stock: float = 0.0
    safety_stock: float = 0.0
    monthly_forecast: float = 0.0
    unit_price: float = 0.0
    
    # Dobavljač
    vendor_id: Optional[int] = None
    
    # COA / Certifikat analize
    has_coa: bool = False
    coa_date: Optional[date] = None
    
    # Batch broj
    batch_number: Optional[str] = None
    
    # Rok isporuke / vremena pružanja
    delivery_time_days: Optional[int] = None
    
    # Minimalna količina narudžbe (MOQ)
    minimum_order_quantity: Optional[float] = None
    moq_unit: Optional[str] = None
    
    # Regulatorni status
    regulatory_status: RegulatoryStatus = RegulatoryStatus.NOT_APPLICABLE
    
    # Skladišni uvjeti
    storage_conditions: Optional[str] = None
    
    # Rok trajanja
    expiry_date: Optional[date] = None
    
    # Analitička metoda
    analytical_method: Optional[str] = None
    
    # Namjena u formulaciji / projektu
    formulation_purpose: Optional[str] = None
    
    # Ugovorni uvjeti
    contract_terms: Optional[str] = None
    
    # Bilješke / napomene
    notes: Optional[str] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    item_type: Optional[ItemType] = None
    material_component: Optional[str] = None
    service_description: Optional[str] = None
    category: Optional[Category] = None
    form: Optional[Form] = None
    standardization: Optional[str] = None
    dose_per_unit: Optional[float] = None
    dose_unit: Optional[str] = None
    total_consumption: Optional[float] = None
    consumption_unit: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    opening_stock: Optional[float] = None
    safety_stock: Optional[float] = None
    monthly_forecast: Optional[float] = None
    unit_price: Optional[float] = None
    vendor_id: Optional[int] = None
    has_coa: Optional[bool] = None
    coa_date: Optional[date] = None
    batch_number: Optional[str] = None
    delivery_time_days: Optional[int] = None
    minimum_order_quantity: Optional[float] = None
    moq_unit: Optional[str] = None
    regulatory_status: Optional[RegulatoryStatus] = None
    storage_conditions: Optional[str] = None
    expiry_date: Optional[date] = None
    analytical_method: Optional[str] = None
    formulation_purpose: Optional[str] = None
    contract_terms: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class MaterialResponse(MaterialBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaterialWithCalculations(MaterialResponse):
    current_stock: float
    recommended_po: float
    stock_status: str  # "normal", "low", "critical"
    last_consumption_date: Optional[datetime] = None
    last_receipt_date: Optional[datetime] = None 