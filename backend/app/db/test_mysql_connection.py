# test_mysql_connection.py
from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Conexión exitosa:", result.scalar())
except Exception as e:
    print("❌ Error al conectar:", e)
