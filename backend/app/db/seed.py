"""
⚠️ ATENCIÓN:
Este archivo solo debe ejecutarse UNA VEZ.
Sirve para insertar datos de prueba iniciales.
Si lo ejecutas otra vez, puede causar errores de claves duplicadas.
"""

from app.db.database import SessionLocal
from app.models.supermarket import Supermarket
from app.models.product import Product
from app.models.supermarket_product import SupermarketProduct
from app.models.ticket import Ticket
from app.models.ticket_item import TicketItem
from datetime import datetime

db = SessionLocal()


# --- Evitar reinserción si la BD ya tiene datos ---
if db.query(Supermarket).first():
    print("⚠️ La base de datos ya tiene datos. Seed cancelado.")
    exit()

# ----- Supermarkets -----
supermarkets = [
    Supermarket(name="Mercadona"),
    Supermarket(name="Carrefour"),
    Supermarket(name="Lidl"),
]
db.add_all(supermarkets)
db.commit()

# ----- Products -----
products = [
    Product(name="Pan"),
    Product(name="Leche"),
    Product(name="Huevos"),
]
db.add_all(products)
db.commit()

# ----- SupermarketProduct -----
# relacionar productos con supermercados y precios
relations = [
    SupermarketProduct(supermarket_id=1, product_id=1, price=1.0),   # Pan Mercadona
    SupermarketProduct(supermarket_id=2, product_id=1, price=1.2),   # Pan Carrefour
    SupermarketProduct(supermarket_id=1, product_id=2, price=0.9),   # Leche Mercadona
]
db.add_all(relations)
db.commit()

# ----- Tickets -----
tickets = [
    Ticket(supermarket_id=1, date=datetime(2025, 11, 24)),  # Ticket Mercadona
]
db.add_all(tickets)
db.commit()

# ----- TicketItems -----
ticket_items = [
    TicketItem(ticket_id=1, product_id=1, quantity=2, price=2.0),
    TicketItem(ticket_id=1, product_id=2, quantity=1, price=0.9),
]
db.add_all(ticket_items)
db.commit()

print("Datos de prueba insertados ✅")
