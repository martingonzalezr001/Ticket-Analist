# app/models/__init__.py
# Importa todos los modelos para que sean recogidos por Alembic / init_db
from app.models.supermarket import Supermarket
from app.models.product import Product
from app.models.supermarket_product import SupermarketProduct
from app.models.ticket import Ticket
from app.models.ticket_item import TicketItem
