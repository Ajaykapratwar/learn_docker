from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from pydantic import BaseModel
from worker import process_delivery
import redis
from config import REDIS_URL

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delivery API")

# Connect to Redis for simple visit caching
redis_client = redis.from_url(REDIS_URL)

class DeliveryCreate(BaseModel):
    item_name: str
    destination: str

@app.get("/")
def read_root():
    visits = redis_client.incr("visits")
    return {"message": "Welcome to the Delivery Logistics API", "visits": visits}

@app.post("/deliveries/")
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = models.Delivery(item_name=delivery.item_name, destination=delivery.destination, status="pending")
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    
    # Send to background worker
    process_delivery.delay(db_delivery.id)
    
    return {"message": "Delivery created and queued for processing", "delivery": db_delivery}

@app.get("/deliveries/{delivery_id}")
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery
