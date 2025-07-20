#!/usr/bin/env python3
"""
Skripta za inicijalizaciju baze podataka s test podacima
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine
from app.core.auth import get_password_hash
from app.models import Base, User, Material, Vendor
from app.models.material import ItemType, Category, Form, RegulatoryStatus
from datetime import datetime, date

def init_db():
    """Inicijalizira bazu podataka s test podacima"""
    
    # Kreiraj tablice
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Provjeri postoje li već podaci
        if db.query(User).first():
            print("Baza podataka već sadrži podatke. Preskačem inicijalizaciju.")
            return
        
        # Kreiraj admin korisnika
        admin_user = User(
            username="admin",
            email="admin@zencore.com",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True,
            role="admin"
        )
        db.add(admin_user)
        
        # Kreiraj test korisnika
        test_user = User(
            username="user",
            email="user@zencore.com",
            full_name="Test User",
            hashed_password=get_password_hash("user123"),
            is_active=True,
            role="user"
        )
        db.add(test_user)
        
        # Kreiraj test dobavljače
        vendors = [
            Vendor(
                code="V001",
                name="Metalurg d.o.o.",
                contact_person="Ivan Horvat",
                email="ivan.horvat@metalurg.hr",
                phone="+385 1 234 5678",
                address="Zagrebačka 123, 10000 Zagreb",
                is_active=True
            ),
            Vendor(
                code="V002",
                name="Kemija Plus",
                contact_person="Marija Novak",
                email="marija.novak@kemijaplus.hr",
                phone="+385 1 345 6789",
                address="Splitska 456, 21000 Split",
                is_active=True
            ),
            Vendor(
                code="V003",
                name="Strojogradnja",
                contact_person="Petar Kovač",
                email="petar.kovac@strojogradnja.hr",
                phone="+385 1 456 7890",
                address="Riječka 789, 51000 Rijeka",
                is_active=True
            ),
            Vendor(
                code="V004",
                name="NutriVita d.o.o.",
                contact_person="Ana Šimić",
                email="ana.simic@nutrivita.hr",
                phone="+385 1 567 8901",
                address="Osječka 321, 31000 Osijek",
                is_active=True
            ),
            Vendor(
                code="V005",
                name="Logistika Pro",
                contact_person="Marko Đurić",
                email="marko.djuric@logistikapro.hr",
                phone="+385 1 678 9012",
                address="Vukovarska 654, 20000 Dubrovnik",
                is_active=True
            )
        ]
        
        for vendor in vendors:
            db.add(vendor)
        
        db.commit()  # Commit da dobijemo ID-jeve vendor-a
        
        # Kreiraj test materijale i usluge
        materials = [
            # Materijali - Adaptogeni
            Material(
                code="M001",
                name="Ashwagandha KSM-66",
                item_type=ItemType.MATERIAL,
                material_component="Withania somnifera",
                category=Category.ADAPTOGEN,
                form=Form.EXTRACT,
                standardization="KSM-66 5% vitanolida",
                dose_per_unit=300.0,
                dose_unit="mg",
                total_consumption=50.0,
                consumption_unit="kg",
                description="Ashwagandha ekstrakt za antistres formulacije",
                unit="kg",
                opening_stock=10.0,
                safety_stock=5.0,
                monthly_forecast=8.0,
                unit_price=150.0,
                vendor_id=4,  # NutriVita
                has_coa=True,
                coa_date=date(2024, 1, 1),
                batch_number="ASH-2024-001",
                delivery_time_days=14,
                minimum_order_quantity=5.0,
                moq_unit="kg",
                regulatory_status=RegulatoryStatus.FOOD_SUPPLEMENT,
                storage_conditions="Temperatura: 15-25°C, RH: <60%, zaštita od svjetla",
                expiry_date=date(2026, 12, 31),
                analytical_method="HPLC",
                formulation_purpose="Antistres, noćni modul",
                notes="Certificiran organic, bez pesticida",
                is_active=True
            ),
            
            # Materijali - Nootropici
            Material(
                code="M002",
                name="Rhodiola Rosea",
                item_type=ItemType.MATERIAL,
                material_component="Rhodiola rosea",
                category=Category.NOOTROPIC,
                form=Form.EXTRACT,
                standardization="3% rosavina / 1% salidrozid",
                dose_per_unit=200.0,
                dose_unit="mg",
                total_consumption=30.0,
                consumption_unit="kg",
                description="Rhodiola ekstrakt za kognitivne formulacije",
                unit="kg",
                opening_stock=8.0,
                safety_stock=3.0,
                monthly_forecast=5.0,
                unit_price=200.0,
                vendor_id=4,  # NutriVita
                has_coa=True,
                coa_date=date(2024, 1, 15),
                batch_number="RHO-2024-001",
                delivery_time_days=21,
                minimum_order_quantity=3.0,
                moq_unit="kg",
                regulatory_status=RegulatoryStatus.FOOD_SUPPLEMENT,
                storage_conditions="Temperatura: 15-25°C, RH: <60%",
                expiry_date=date(2026, 6, 30),
                analytical_method="HPLC",
                formulation_purpose="Brzo djelovanje, fokus",
                notes="Wildcrafted iz Sibira",
                is_active=True
            ),
            
            # Materijali - Vitamini
            Material(
                code="M003",
                name="Vitamin D3",
                item_type=ItemType.MATERIAL,
                material_component="Cholecalciferol",
                category=Category.VITAMIN,
                form=Form.POWDER,
                standardization="100,000 IU/g",
                dose_per_unit=1000.0,
                dose_unit="IU",
                total_consumption=20.0,
                consumption_unit="kg",
                description="Vitamin D3 u prašku za kapsule",
                unit="kg",
                opening_stock=5.0,
                safety_stock=2.0,
                monthly_forecast=3.0,
                unit_price=300.0,
                vendor_id=2,  # Kemija Plus
                has_coa=True,
                coa_date=date(2024, 2, 1),
                batch_number="VD3-2024-001",
                delivery_time_days=7,
                minimum_order_quantity=1.0,
                moq_unit="kg",
                regulatory_status=RegulatoryStatus.APPROVED,
                storage_conditions="Temperatura: 2-8°C, zaštita od svjetla",
                expiry_date=date(2025, 12, 31),
                analytical_method="HPLC",
                formulation_purpose="Imunološka podrška",
                notes="Vegetarijanski, bez GMO",
                is_active=True
            ),
            
            # Usluge - Proizvodnja
            Material(
                code="S001",
                name="Proizvodnja kapsula",
                item_type=ItemType.SERVICE,
                service_description="Proizvodnja hard gel kapsula",
                category=Category.PRODUCTION,
                dose_per_unit=1.0,
                dose_unit="lot",
                total_consumption=24.0,
                consumption_unit="lot",
                description="Proizvodnja kapsula u lotovima od 10,000 kom",
                unit="lot",
                opening_stock=0.0,
                safety_stock=0.0,
                monthly_forecast=2.0,
                unit_price=5000.0,
                vendor_id=3,  # Strojogradnja
                has_coa=False,
                delivery_time_days=30,
                minimum_order_quantity=1.0,
                moq_unit="lot",
                regulatory_status=RegulatoryStatus.APPROVED,
                storage_conditions="Nije primjenjivo",
                analytical_method="Nije primjenjivo",
                formulation_purpose="Faza proizvodnje",
                contract_terms="Godišnji ugovor, 2 lota mjesečno",
                notes="GMP certificirana proizvodnja",
                is_active=True
            ),
            
            # Usluge - Pakiranje
            Material(
                code="S002",
                name="Pakiranje i etiketiranje",
                item_type=ItemType.SERVICE,
                service_description="Pakiranje u boce i etiketiranje",
                category=Category.PACKAGING,
                dose_per_unit=1.0,
                dose_unit="lot",
                total_consumption=24.0,
                consumption_unit="lot",
                description="Pakiranje u boce od 60 kapsula",
                unit="lot",
                opening_stock=0.0,
                safety_stock=0.0,
                monthly_forecast=2.0,
                unit_price=3000.0,
                vendor_id=3,  # Strojogradnja
                has_coa=False,
                delivery_time_days=15,
                minimum_order_quantity=1.0,
                moq_unit="lot",
                regulatory_status=RegulatoryStatus.APPROVED,
                storage_conditions="Nije primjenjivo",
                analytical_method="Nije primjenjivo",
                formulation_purpose="Faza pakiranja",
                contract_terms="Po potrebi, 15 dana rok",
                notes="Automatsko pakiranje s kontrolom kvalitete",
                is_active=True
            ),
            
            # Usluge - Prijevoz
            Material(
                code="S003",
                name="Hladnjački prijevoz",
                item_type=ItemType.SERVICE,
                service_description="Hladnjački prijevoz temperature osjetljivih materijala",
                category=Category.TRANSPORT,
                dose_per_unit=1.0,
                dose_unit="tura",
                total_consumption=48.0,
                consumption_unit="tura",
                description="Prijevoz u kontroliranoj temperaturi",
                unit="tura",
                opening_stock=0.0,
                safety_stock=0.0,
                monthly_forecast=4.0,
                unit_price=800.0,
                vendor_id=5,  # Logistika Pro
                has_coa=False,
                delivery_time_days=3,
                minimum_order_quantity=1.0,
                moq_unit="tura",
                regulatory_status=RegulatoryStatus.APPROVED,
                storage_conditions="Nije primjenjivo",
                analytical_method="Nije primjenjivo",
                formulation_purpose="Logistika",
                contract_terms="Po potrebi, 24h najava",
                notes="GPS praćenje, temperature monitoring",
                is_active=True
            )
        ]
        
        for material in materials:
            db.add(material)
        
        # Spremi sve promjene
        db.commit()
        
        print("Baza podataka uspješno inicijalizirana s test podacima!")
        print("\nTest korisnici:")
        print("- Username: admin, Password: admin123")
        print("- Username: user, Password: user123")
        print("\nKreirani su test materijali, usluge i dobavljači.")
        print("\nMaterijali uključuju:")
        print("- Adaptogene (Ashwagandha, Rhodiola)")
        print("- Vitamine (D3)")
        print("- Usluge (proizvodnja, pakiranje, prijevoz)")
        
    except Exception as e:
        print(f"Greška pri inicijalizaciji baze: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 