# app/routes/ocr_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ocr.engine import save_temp_file, run_ocr
from app.ocr.parser import parse_ticket_text

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/scan")
async def ocr_scan(file: UploadFile = File(...)):
    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Formato no soportado")

    file_bytes = await file.read()

    # guardar temporal
    image_path, image_id = save_temp_file(file_bytes)

    # ejecutar OCR
    lines = run_ocr(image_path)

    # parsear texto detectado
    items = parse_ticket_text(lines)

    return {
        "image_id": image_id,
        "lines_detected": lines,
        "items_detected": items
    }

# Recibe imagen
@router.get("/retry/{image_id}")
async def ocr_retry(image_id: str):
    import os
    from app.ocr.engine import BASE_TEMP_DIR

    # buscar archivo temporal
    files = os.listdir(BASE_TEMP_DIR)
    candidates = [f for f in files if f.startswith(image_id)]

    if not candidates:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_path = os.path.join(BASE_TEMP_DIR, candidates[0])

    lines = run_ocr(image_path)
    items = parse_ticket_text(lines)

    return {
        "image_id": image_id,
        "lines_detected": lines,
        "items_detected": items
    }
