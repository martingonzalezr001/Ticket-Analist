from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class TicketItemConfirm(BaseModel):
    product_id: Optional[int]
    name: str
    quantity: float
    price: float

class TicketConfirm(BaseModel):
    supermarket_id: int
    date: date
    total: float
    items: List[TicketItemConfirm]
