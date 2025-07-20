from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class ItemType(enum.Enum):
    MATERIAL = "materijal"
    SERVICE = "usluga"


class Category(enum.Enum):
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


class Form(enum.Enum):
    POWDER = "prašak"
    CAPSULE = "kapsula"
    OIL = "ulje"
    EXTRACT = "ekstrakt"
    LIPOSOME = "liposom"
    MICROENCAPSULATED = "mikroenkapsula"
    TABLET = "tableta"
    LIQUID = "tekućina"
    OTHER = "ostalo"


class RegulatoryStatus(enum.Enum):
    NOVEL_FOOD = "novel_food"
    FOOD_SUPPLEMENT = "dodatak_prehrani"
    SCHOOL_BAN = "školska_zabrana"
    APPROVED = "odobreno"
    PENDING = "na_čekanju"
    NOT_APPLICABLE = "nije_primjenjivo"


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    
    # Tip stavke
    item_type = Column(Enum(ItemType), nullable=False, default=ItemType.MATERIAL)
    
    # Materijal / Sastojak (za materijale)
    material_component = Column(String)  # Sastojak materijala
    
    # Opis usluge
    service_description = Column(Text)  # Opis usluge (proizvodnja, pakiranje, itd.)
    
    # Kategorija
    category = Column(Enum(Category), nullable=False)
    
    # Oblik
    form = Column(Enum(Form))
    
    # Standardizacija / Specifikacija
    standardization = Column(String)  # "KSM-66 5% vitanolida", "3% rosavina / 1% salidrozid"
    
    # Doza po jedinici
    dose_per_unit = Column(Float)  # mg ili µg po kapsuli/porciji
    dose_unit = Column(String)  # mg, µg, sat, lot, tura
    
    # Ukupna potrošnja / obujam
    total_consumption = Column(Float)  # godišnja količina u kg, mL
    consumption_unit = Column(String)  # kg, mL, sat, lot, tura
    
    # Osnovne informacije
    description = Column(Text)
    unit = Column(String, nullable=False)  # kg, kom, m, sat, lot, etc.
    opening_stock = Column(Float, default=0.0)
    safety_stock = Column(Float, default=0.0)  # Sigurnosna zaliha
    monthly_forecast = Column(Float, default=0.0)  # Mjesečni forecast
    unit_price = Column(Float, default=0.0)
    
    # Dobavljač
    vendor_id = Column(Integer, nullable=True)
    
    # COA / Certifikat analize
    has_coa = Column(Boolean, default=False)
    coa_date = Column(Date)
    
    # Batch broj
    batch_number = Column(String)
    
    # Rok isporuke / vremena pružanja
    delivery_time_days = Column(Integer)  # dani ili tjedni
    
    # Minimalna količina narudžbe (MOQ)
    minimum_order_quantity = Column(Float)
    moq_unit = Column(String)
    
    # Regulatorni status
    regulatory_status = Column(Enum(RegulatoryStatus), default=RegulatoryStatus.NOT_APPLICABLE)
    
    # Skladišni uvjeti
    storage_conditions = Column(Text)  # temp. / RH / zaštita od svjetla
    
    # Rok trajanja
    expiry_date = Column(Date)
    
    # Analitička metoda
    analytical_method = Column(String)  # HPLC, DLS, UV-Vis
    
    # Namjena u formulaciji / projektu
    formulation_purpose = Column(Text)  # brzo djelovanje, antistres, noćni modul
    
    # Ugovorni uvjeti
    contract_terms = Column(Text)  # trajanje ugovora, vertikalni zakres usluge
    
    # Bilješke / napomene
    notes = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    vendor = relationship("Vendor", back_populates="materials")
    offers = relationship("Offer", back_populates="material")
    purchase_orders = relationship("PurchaseOrder", back_populates="material")
    receipts = relationship("Receipt", back_populates="material")
    consumptions = relationship("Consumption", back_populates="material")

    # Indeksi za optimizaciju
    __table_args__ = (
        Index('idx_material_code', 'code'),
        Index('idx_material_type', 'item_type'),
        Index('idx_material_category', 'category'),
        Index('idx_material_vendor', 'vendor_id'),
        Index('idx_material_active', 'is_active'),
        Index('idx_material_coa', 'has_coa'),
        Index('idx_material_regulatory', 'regulatory_status'),
    ) 