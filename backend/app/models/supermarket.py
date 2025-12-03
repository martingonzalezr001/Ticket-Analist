# app/models/supermarket.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Supermarket(Base):
    __tablename__ = "supermarkets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    branch = Column(String(200), nullable=True)  # sucursal / dirección opcional

    tickets = relationship("Ticket", back_populates="supermarket", cascade="all, delete-orphan")
    supermarket_products = relationship("SupermarketProduct", back_populates="supermarket", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Supermarket(id={self.id}, name={self.name})>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "branch": self.branch}
