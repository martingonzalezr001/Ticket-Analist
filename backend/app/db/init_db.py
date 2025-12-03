# app/db/init_db.py
from app.db.database import Base, engine
# importa modelos para que sean registrados en metadata
from app.models import supermarket, product, supermarket_product, ticket, ticket_item

def run():
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas ✅")

if __name__ == "__main__":
    run()
