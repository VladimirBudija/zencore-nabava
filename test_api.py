#!/usr/bin/env python3
"""
Skripta za testiranje ZenCore API-ja
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    """Testira osnovne API endpointi"""
    
    print("🧪 Testiranje ZenCore API-ja")
    print("=" * 50)
    
    # 1. Test health check
    print("\n1. Health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # 2. Registracija korisnika
    print("\n2. Registracija test korisnika...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 200:
            print("✅ Registracija uspješna")
        else:
            print(f"❌ Registracija failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Registracija error: {e}")
    
    # 3. Login
    print("\n3. Login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("✅ Login uspješan")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Headers za autentificirane zahtjeve
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. Kreiranje materijala
    print("\n4. Kreiranje test materijala...")
    material_data = {
        "code": "TEST001",
        "name": "Test Materijal",
        "description": "Materijal za testiranje",
        "unit": "kom",
        "opening_stock": 100.0,
        "safety_stock": 20.0,
        "monthly_forecast": 50.0,
        "unit_price": 10.0,
        "category": "repromaterijal"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/materials", json=material_data, headers=headers)
        if response.status_code == 200:
            material = response.json()
            material_id = material["id"]
            print("✅ Materijal kreiran")
        else:
            print(f"❌ Kreiranje materijala failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Kreiranje materijala error: {e}")
        return
    
    # 5. Dohvaćanje materijala s kalkulacijama
    print("\n5. Dohvaćanje materijala s kalkulacijama...")
    try:
        response = requests.get(f"{BASE_URL}/materials/{material_id}", headers=headers)
        if response.status_code == 200:
            material_with_calc = response.json()
            print(f"✅ Materijal dohvaćen")
            print(f"   - Trenutna zaliha: {material_with_calc['current_stock']}")
            print(f"   - Preporučena narudžba: {material_with_calc['recommended_po']}")
            print(f"   - Status zaliha: {material_with_calc['stock_status']}")
        else:
            print(f"❌ Dohvaćanje materijala failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dohvaćanje materijala error: {e}")
    
    # 6. Dashboard summary
    print("\n6. Dashboard summary...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/summary", headers=headers)
        if response.status_code == 200:
            dashboard = response.json()
            print("✅ Dashboard dohvaćen")
            print(f"   - Ukupan broj materijala: {dashboard['total_materials']}")
            print(f"   - Materijali s niskim zalihama: {dashboard['low_stock_materials_count']}")
            print(f"   - Aktivne narudžbe: {dashboard['active_purchase_orders']}")
        else:
            print(f"❌ Dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
    
    # 7. Kreiranje prijema
    print("\n7. Kreiranje test prijema...")
    receipt_data = {
        "receipt_number": "R001",
        "material_id": material_id,
        "vendor_id": 1,  # Pretpostavljamo da postoji vendor s ID 1
        "quantity": 50.0,
        "unit_price": 9.5,
        "total_amount": 475.0,
        "receipt_date": datetime.now().isoformat(),
        "notes": "Test prijem"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/receipts", json=receipt_data, headers=headers)
        if response.status_code == 200:
            print("✅ Prijem kreiran")
        else:
            print(f"❌ Kreiranje prijema failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Kreiranje prijema error: {e}")
    
    # 8. Kreiranje utroška
    print("\n8. Kreiranje test utroška...")
    consumption_data = {
        "consumption_number": "C001",
        "material_id": material_id,
        "quantity": 10.0,
        "consumption_date": datetime.now().isoformat(),
        "project": "Test Projekt",
        "cost_center": "CC001",
        "notes": "Test utrošak"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/consumptions", json=consumption_data, headers=headers)
        if response.status_code == 200:
            print("✅ Utrošak kreiran")
        else:
            print(f"❌ Kreiranje utroška failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Kreiranje utroška error: {e}")
    
    # 9. Ponovno dohvaćanje materijala s ažuriranim kalkulacijama
    print("\n9. Ponovno dohvaćanje materijala s ažuriranim kalkulacijama...")
    try:
        response = requests.get(f"{BASE_URL}/materials/{material_id}", headers=headers)
        if response.status_code == 200:
            material_with_calc = response.json()
            print(f"✅ Materijal dohvaćen s ažuriranim kalkulacijama")
            print(f"   - Trenutna zaliha: {material_with_calc['current_stock']}")
            print(f"   - Preporučena narudžba: {material_with_calc['recommended_po']}")
            print(f"   - Status zaliha: {material_with_calc['stock_status']}")
        else:
            print(f"❌ Dohvaćanje materijala failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dohvaćanje materijala error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testiranje završeno!")
    print("\nAPI je spreman za korištenje.")
    print("Pristupite Swagger dokumentaciji na: http://localhost:8000/docs")

if __name__ == "__main__":
    test_api() 