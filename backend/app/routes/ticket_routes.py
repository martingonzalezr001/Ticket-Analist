# app/routes/ticket_routes.py

from fastapi import APIRouter, Depends, HTTPException;
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.ticket import Ticket
from app.models.ticket_item import TicketItem
from app.schemas.ticket import TicketConfirm

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
def confirm_ticket(
    data: TicketConfirm,
    db: Session = Depends(get_db)
):
    if not data.items:
        raise HTTPException(
            status_code=400,
            detail="El ticket no contiene items"
        )

    try:
        # 1️⃣ Crear ticket
        ticket = Ticket(
            supermarket_id=data.supermarket_id,
            date=data.date,
            total=data.total
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        # 2️⃣ Crear items
        for item in data.items:
            db_item = TicketItem(
                ticket_id=ticket.id,
                product_id=item.product_id,
                raw_name=item.name,
                quantity=item.quantity,
                price=item.price
            )
            db.add(db_item)

        db.commit()

        return {
            "status": "saved",
            "ticket_id": ticket.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error guardando el ticket"
        )