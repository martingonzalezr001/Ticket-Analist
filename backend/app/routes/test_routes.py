# comprobar que la API está viva
# usado por tests, docker, CI/CD, monitoreo
# no toca BD
#
# Nunca se elimina, es básico.
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"message": "API running correctly"}
