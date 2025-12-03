from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.supermarket_product import SupermarketProduct

router = APIRouter()

@router.get("/supermarket-products")
def get_supermarket_products(db: Session = Depends(get_db)):
    return db.query(SupermarketProduct).all()
