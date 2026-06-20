from PIL import Image
from pathlib import Path

def extract_text_from_image(image_path: str) -> str:
    try:
        import pytesseract
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[Image processing unavailable: {str(e)}]"

def process_image(image_path: str):
    text = extract_text_from_image(image_path)
    return {
        "text": text,
        "source": Path(image_path).name,
        "type": "image",
        "pages": 1
    }