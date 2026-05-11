from sqlalchemy import Column, Integer, String
from database import Base

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    destination = Column(String)
    status = Column(String, default="pending")
