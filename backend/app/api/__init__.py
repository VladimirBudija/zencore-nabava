from .auth import router as auth_router
from .materials import router as materials_router
from .vendors import router as vendors_router
from .offers import router as offers_router
from .purchase_orders import router as purchase_orders_router
from .receipts import router as receipts_router
from .consumptions import router as consumptions_router
from .dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "materials_router", 
    "vendors_router",
    "offers_router",
    "purchase_orders_router",
    "receipts_router",
    "consumptions_router",
    "dashboard_router"
] 