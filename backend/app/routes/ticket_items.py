from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.ticket_item import TicketItem

router = APIRouter()

@router.get("/ticket-items")
def get_ticket_items(db: Session = Depends(get_db)):
    return db.query(TicketItem).all()
