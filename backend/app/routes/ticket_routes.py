# app/routes/ticket_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.ticket import Ticket
from app.models.ticket_item import TicketItem

router = APIRouter(prefix="/tickets", tags=["Tickets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()

@router.post("/confirm")
def confirm_ticket(data: dict, db: Session = Depends(get_db)):
    # data viene del frontend tras revisión
    ticket = Ticket(
        supermarket_id=data["supermarket_id"],
        date=data["date"],
        total=data["total"]
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    for item in data["items"]:
        db_item = TicketItem(
            ticket_id=ticket.id,
            product_id=item.get("product_id"),  # puede ser null
            raw_name=item["raw"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.add(db_item)

    db.commit()

    return {"status": "saved", "ticket_id": ticket.id}
