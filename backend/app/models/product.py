# app/models/product.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(150), nullable=True)
    category = Column(String(150), nullable=True)
    unit = Column(String(50), nullable=True)  # ej: 'unidad', 'kg', 'l'

    supermarket_products = relationship("SupermarketProduct", back_populates="product", cascade="all, delete-orphan")
    ticket_items = relationship("TicketItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "brand": self.brand, "category": self.category, "unit": self.unit}
