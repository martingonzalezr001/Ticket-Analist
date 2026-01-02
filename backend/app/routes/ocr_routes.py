# app/routes/ocr_routes.py
'''
Flujo real: 
POST /ocr/preview
        ↓
Usuario revisa datos
        ↓
POST /tickets/confirm
        ↓
Guardado en BD
'''

# app/routes/ocr_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ocr.engine import save_temp_file, run_ocr
from app.ocr.parser import parse_ticket_text
import os

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/preview")
async def ocr_preview(file: UploadFile = File(...)):
    # 1️⃣ Validación básica
    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {file.content_type}"
        )

    # 2️⃣ Guardar imagen temporal
    content = await file.read()
    image_path, image_id = save_temp_file(content)

    try:
        # 3️⃣ Ejecutar OCR
        ocr_lines = run_ocr(image_path)

        # 4️⃣ Parsear texto OCR
        parsed_items = parse_ticket_text(ocr_lines)

        # 5️⃣ Construir payload de preview
        response = {
            "image_id": image_id,
            "status": "preview",
            "supermarket": {
                "raw": None,
                "normalized": None,
                "confidence": None
            },
            "ticket": {
                "date": {
                    "raw": None,
                    "parsed": None,
                    "confidence": None
                },
                "total": {
                    "raw": None,
                    "parsed": None,
                    "confidence": None
                }
            },
            "items": [],
            "summary": {
                "items_detected": len(parsed_items),
                "items_with_low_confidence": 0,
                "total_matches_sum": sum(
                    item["price"] for item in parsed_items if item.get("price")
                ),
                "total_detected": None,
                "total_difference": None
            },
            "warnings": [],
            "next_actions": {
                "confirm_endpoint": "/tickets/confirm",
                "retry_endpoint": f"/ocr/retry/{image_id}"
            }
        }

        # 6️⃣ Convertir items al formato frontend
        for idx, item in enumerate(parsed_items, start=1):
            response["items"].append({
                "line_id": idx,
                "raw_text": item["raw"],
                "product": {
                    "raw": item["name"],
                    "normalized": item["name"].title(),
                    "product_id": None
                },
                "quantity": {
                    "raw": str(item.get("quantity", 1)),
                    "parsed": item.get("quantity", 1),
                    "confidence": 0.9
                },
                "price": {
                    "raw": str(item["price"]),
                    "parsed": item["price"],
                    "confidence": 0.9
                },
                "price_per_kg": None,
                "warnings": []
            })

        return response

    finally:
        # 7️⃣ Limpieza del archivo temporal
        if os.path.exists(image_path):
            os.remove(image_path)
