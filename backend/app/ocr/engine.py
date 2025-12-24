# app/ocr/engine.py
import uuid
import os
from paddleocr import PaddleOCR

BASE_TEMP_DIR = "app/ocr/temp/"

ocr_model = PaddleOCR(use_angle_cls=True, lang='es')

def save_temp_file(upload_file) -> str:
    """Guarda archivo subido en carpeta temporal y devuelve ruta."""
    file_id = str(uuid.uuid4())
    ext = upload_file.filename.split(".")[-1]
    filename = f"{file_id}.{ext}"

    path = os.path.join(BASE_TEMP_DIR, filename)

    with open(path, "wb") as f:
        f.write(upload_file)

    return path, file_id

def run_ocr(image_path: str):
    result = ocr_model.ocr(image_path, cls=True)

    lines = []
    for page in result:
        for box, (text, score) in page:
            lines.append({"text": text, "confidence": float(score)})

    return lines
