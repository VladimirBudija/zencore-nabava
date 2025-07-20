from celery.schedules import crontab
from app.celery_app import celery_app

# Konfiguracija periodičnih taskova
celery_app.conf.beat_schedule = {
    # Noćna sync s ERP-om - svaki dan u 2:00
    'sync-with-erp-daily': {
        'task': 'app.tasks.sync_with_erp',
        'schedule': crontab(hour=2, minute=0),
    },
    
    # Dnevne obavijesti o niskim zalihama - svaki dan u 9:00
    'send-low-stock-notifications-daily': {
        'task': 'app.tasks.send_low_stock_notifications',
        'schedule': crontab(hour=9, minute=0),
    },
    
    # Dnevni izvještaj - svaki dan u 18:00
    'daily-report': {
        'task': 'app.tasks.daily_report',
        'schedule': crontab(hour=18, minute=0),
    },
    
    # Provjera niskih zaliha - svaki sat
    'check-low-stock-hourly': {
        'task': 'app.tasks.send_low_stock_notifications',
        'schedule': crontab(minute=0),  # Svaki sat
    },
} 