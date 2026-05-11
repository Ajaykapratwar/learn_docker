from celery import Celery
from config import REDIS_URL
from database import SessionLocal
from models import Delivery
import time

celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(name="process_delivery")
def process_delivery(delivery_id: int):
    # Simulate background processing (e.g., assigning a driver, calculating route)
    time.sleep(5)
    
    db = SessionLocal()
    try:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if delivery:
            delivery.status = "dispatched"
            db.commit()
    finally:
        db.close()
        
    return f"Delivery {delivery_id} dispatched."
