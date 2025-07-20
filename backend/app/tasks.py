import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from sqlalchemy.orm import Session
from .celery_app import celery_app
from .core.database import SessionLocal
from .core.config import settings
from .services.material_service import MaterialService
from .models.material import Material


@celery_app.task
def sync_with_erp():
    """Noćna sync funkcija prema ERP sustavu (placeholder)"""
    try:
        # Placeholder za ERP sync
        # U stvarnoj implementaciji ovdje bi bio kod za povezivanje s ERP sustavom
        
        # Simuliraj API poziv prema ERP-u
        erp_endpoint = "https://erp.company.com/api/materials/sync"
        
        # Ovdje bi bio stvarni kod za sync
        # response = httpx.get(erp_endpoint, timeout=30)
        
        print(f"ERP sync completed at {datetime.utcnow()}")
        return {"status": "success", "message": "ERP sync completed"}
        
    except Exception as e:
        print(f"ERP sync failed: {str(e)}")
        return {"status": "error", "message": str(e)}


@celery_app.task
def send_low_stock_notifications():
    """Dnevno slanje obavijesti za materijale ispod sigurnosne zalihe"""
    try:
        db = SessionLocal()
        
        # Dohvati materijale s niskim zalihama
        low_stock_materials = MaterialService.get_low_stock_materials(db)
        
        if not low_stock_materials:
            print("No low stock materials found")
            return {"status": "success", "message": "No notifications sent"}
        
        # Pripremi poruku
        message = "Materijali s niskim zalihama:\n\n"
        for material in low_stock_materials:
            message += f"- {material.code}: {material.name}\n"
            message += f"  Trenutna zaliha: {material.current_stock} {material.unit}\n"
            message += f"  Sigurnosna zaliha: {material.safety_stock} {material.unit}\n"
            message += f"  Preporučena narudžba: {material.recommended_po} {material.unit}\n\n"
        
        # Pošalji e-mail obavijest (ako je konfiguriran)
        if settings.smtp_server:
            send_email_notification(message)
        
        # Pošalji Slack obavijest (ako je konfiguriran)
        if settings.slack_webhook_url:
            send_slack_notification(message)
        
        print(f"Low stock notifications sent for {len(low_stock_materials)} materials")
        return {
            "status": "success", 
            "message": f"Notifications sent for {len(low_stock_materials)} materials"
        }
        
    except Exception as e:
        print(f"Low stock notifications failed: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


def send_email_notification(message: str):
    """Pošalji e-mail obavijest"""
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.smtp_username
        msg['To'] = "admin@company.com"  # U produkciji bi bio dinamički
        msg['Subject'] = "ZenCore - Obavijest o niskim zalihama"
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        
        print("Email notification sent successfully")
        
    except Exception as e:
        print(f"Email notification failed: {str(e)}")


def send_slack_notification(message: str):
    """Pošalji Slack obavijest"""
    try:
        slack_data = {
            "text": f"🚨 *ZenCore - Obavijest o niskim zalihama*\n\n{message}"
        }
        
        response = httpx.post(
            settings.slack_webhook_url,
            json=slack_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("Slack notification sent successfully")
        else:
            print(f"Slack notification failed: {response.status_code}")
            
    except Exception as e:
        print(f"Slack notification failed: {str(e)}")


@celery_app.task
def daily_report():
    """Dnevni izvještaj o stanju zaliha"""
    try:
        db = SessionLocal()
        
        # Dohvati sve aktivne materijale
        materials = db.query(Material).filter(Material.is_active == True).all()
        
        report_data = {
            "date": datetime.utcnow().isoformat(),
            "total_materials": len(materials),
            "materials_summary": []
        }
        
        for material in materials:
            current_stock = MaterialService.calculate_current_stock(db, material.id)
            stock_status = MaterialService.get_stock_status(db, material.id)
            
            report_data["materials_summary"].append({
                "code": material.code,
                "name": material.name,
                "current_stock": current_stock,
                "safety_stock": material.safety_stock,
                "status": stock_status
            })
        
        # Ovdje bi se report spremio u bazu ili poslao na e-mail
        print(f"Daily report generated for {len(materials)} materials")
        
        return {"status": "success", "data": report_data}
        
    except Exception as e:
        print(f"Daily report failed: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close() 