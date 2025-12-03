from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.ticket import Ticket

router = APIRouter()

@router.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()


