# app/models/ticket.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total = Column(Float, nullable=True)

    supermarket = relationship("Supermarket", back_populates="tickets")
    items = relationship("TicketItem", back_populates="ticket", cascade="all, delete-orphan")
    products = relationship(
    "Product",
    secondary="ticket_items",
    viewonly=True
)