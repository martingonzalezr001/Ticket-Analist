# app/ocr/parser.py

def parse_ticket_text(ocr_lines):
    items = []

    for line in ocr_lines:
        text = line["text"]

        # Ejemplo básico: detectar algo tipo "PAN 1.20"
        parts = text.rsplit(" ", 1)

        if len(parts) == 2 and parts[1].replace(".", "", 1).isdigit():
            name = parts[0]
            price = float(parts[1])
            items.append({
                "raw": text,
                "name": name,
                "quantity": 1,
                "price": price
            })

    return items
