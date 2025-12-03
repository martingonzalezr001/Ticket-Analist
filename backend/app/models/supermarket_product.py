# app/models/supermarket_product.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class SupermarketProduct(Base):
    __tablename__ = "supermarket_products"
    __table_args__ = (
        UniqueConstraint("supermarket_id", "product_id", name="uix_supermarket_product"),
    )

    id = Column(Integer, primary_key=True, index=True)
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    supermarket = relationship("Supermarket", back_populates="supermarket_products")
    product = relationship("Product", back_populates="supermarket_products")

    def __repr__(self):
        return f"<SupermarketProduct(id={self.id}, supermarket_id={self.supermarket_id}, product_id={self.product_id}, price={self.price})>"

    def to_dict(self):
        return {"id": self.id, "supermarket_id": self.supermarket_id, "product_id": self.product_id, "price": float(self.price), "registered_at": self.registered_at.isoformat()}
