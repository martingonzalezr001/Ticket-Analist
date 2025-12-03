from fastapi import FastAPI
from app.utils import config
from app.utils.logger import logger

from app.routes import supermarket_products, tickets, ticket_items, test_routes
from app.routes import product_routes, supermarket_routes

app = FastAPI(title=config.APP_NAME)

# Endpoints de prueba
app.include_router(test_routes.router)
app.include_router(supermarket_routes.router)
app.include_router(product_routes.router)
app.include_router(supermarket_products.router)
app.include_router(tickets.router)
app.include_router(ticket_items.router)

@app.get("/ping")
def ping():
    return {"status": "ok", "debug": config.DEBUG}

logger.info("Backend iniciado correctamente Vamos Allá")
