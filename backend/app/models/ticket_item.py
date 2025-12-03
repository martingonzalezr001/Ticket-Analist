# app/models/ticket_item.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class TicketItem(Base):
    __tablename__ = "ticket_items"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)  # puede ser NULL si no hay match
    raw_name = Column(String(500), nullable=False)  # texto detectado por OCR
    quantity = Column(Float, nullable=True)
    price = Column(Numeric(10,2), nullable=True)  # precio cobrado en el ticket
    price_per_kg = Column(Numeric(10,2), nullable=True)

    ticket = relationship("Ticket", back_populates="items")
    product = relationship("Product", back_populates="ticket_items")

    def __repr__(self):
        return f"<TicketItem(id={self.id}, ticket_id={self.ticket_id}, raw_name={self.raw_name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "product_id": self.product_id,
            "raw_name": self.raw_name,
            "quantity": self.quantity,
            "price": float(self.price) if self.price is not None else None,
            "price_per_kg": float(self.price_per_kg) if self.price_per_kg is not None else None
        }
