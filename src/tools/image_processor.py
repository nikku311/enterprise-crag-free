from PIL import Image
import pytesseract
from pathlib import Path

def extract_text_from_image(image_path: str) -> str:
    """Extract text from image using OCR"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def process_image(image_path: str):
    """Process image and return text + metadata"""
    text = extract_text_from_image(image_path)
    
    return {
        "text": text,
        "source": Path(image_path).name,
        "type": "image",
        "pages": 1
    }

if __name__ == "__main__":
    # Test
    print("Image processor ready - needs image file to test")