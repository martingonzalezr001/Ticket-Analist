from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["Products"])
# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#-------- GET ALL --------
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


#-------- GET ONE BY ID --------
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



# --- CREATE ---
@router.post("/")
def create_product(name: str, brand: str | None = None, category: str | None = None, unit: str | None = None, db: Session = Depends(get_db)):
    product = Product(name=name, brand=brand, category=category, unit=unit)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
# --- DELETE ---
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
