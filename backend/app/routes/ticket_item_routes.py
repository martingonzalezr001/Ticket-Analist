from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.ticket_item import TicketItem

router = APIRouter()

@router.get("/ticket-items")
def get_ticket_items(db: Session = Depends(get_db)):
    return db.query(TicketItem).all()


@router.get("/ticket-items/{ticket_id}")
def get_ticket_items_by_ticket(ticket_id: int, db: Session = Depends(get_db)):
    items = db.query(TicketItem).filter(TicketItem.ticket_id == ticket_id).all()

    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No hay items para el ticket con id {ticket_id}"
        )

    return items