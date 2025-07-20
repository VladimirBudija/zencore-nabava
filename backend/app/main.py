from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
from .core.database import engine
from .models import Base
from .api import (
    auth_router,
    materials_router,
    vendors_router,
    offers_router,
    purchase_orders_router,
    receipts_router,
    consumptions_router,
    dashboard_router
)

# Pokreni migracije ako je potrebno
def run_migrations():
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Migracije uspješno pokrenute")
    except Exception as e:
        print(f"⚠️ Greška pri migracijama: {e}")

# Inicijaliziraj bazu ako je potrebno
def init_database():
    try:
        from .init_db import init_db
        init_db()
        print("✅ Baza podataka inicijalizirana")
    except Exception as e:
        print(f"⚠️ Greška pri inicijalizaciji baze: {e}")

# Kreiraj tablice i pokreni migracije
Base.metadata.create_all(bind=engine)
run_migrations()

# Inicijaliziraj bazu ako je postavljena varijabla
if os.getenv("INIT_DB", "false").lower() == "true":
    init_database()

app = FastAPI(
    title="ZenCore API",
    description="Sustav za materijalno knjigovodstvo",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # U produkciji postavi specifične domene
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uključi routere
app.include_router(auth_router)
app.include_router(materials_router)
app.include_router(vendors_router)
app.include_router(offers_router)
app.include_router(purchase_orders_router)
app.include_router(receipts_router)
app.include_router(consumptions_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    return {
        "message": "ZenCore API - Sustav za materijalno knjigovodstvo",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 