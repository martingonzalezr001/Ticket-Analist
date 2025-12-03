from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.supermarket import Supermarket

router = APIRouter(prefix="/supermarkets", tags=["Supermarkets"])

# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- GET ALL ---
@router.get("/")
def get_supermarkets(db: Session = Depends(get_db)):
    return db.query(Supermarket).all()

# --- GET ONE BY ID ---
@router.get("/{supermarket_id}")
def get_supermarket(supermarket_id: int, db: Session = Depends(get_db)):
    supermarket = db.query(Supermarket).filter(Supermarket.id == supermarket_id).first()
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    return supermarket

# --- CREATE ---
@router.post("/")
def create_supermarket(name: str, branch: str | None = None, db: Session = Depends(get_db)):
    new_supermarket = Supermarket(name=name, branch=branch)
    db.add(new_supermarket)
    db.commit()
    db.refresh(new_supermarket)
    return new_supermarket

# --- DELETE ---
@router.delete("/{supermarket_id}")
def delete_supermarket(supermarket_id: int, db: Session = Depends(get_db)):
    supermarket = db.query(Supermarket).filter(Supermarket.id == supermarket_id).first()
    if not supermarket:
        raise HTTPException(status_code=404, detail="Supermarket not found")
    db.delete(supermarket)
    db.commit()
    return {"message": "Supermarket deleted"}
