import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes

def extract_text_from_image(image_file):
    img = Image.open(image_file)
    return pytesseract.image_to_string(img)

def extract_text_from_pdf(file):
    text = ""

    # Convert PDF pages to images
    images = convert_from_bytes(file.read(), dpi=300)
    for img in images:
        # Optional: enhance image for better OCR
        img = img.convert('L')  # grayscale
        img = img.point(lambda p: 0 if isinstance(p, int) and p < 140 else 255, '1')  # binarize
        text += pytesseract.image_to_string(img) + "\n"

    return text

def extract_text(file, filename):
    if filename.endswith((".jpg", ".png")):
        return extract_text_from_image(file)
    elif filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")
