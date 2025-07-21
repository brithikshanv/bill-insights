import pytesseract
from PIL import Image
import fitz  # PyMuPDF

def extract_text_from_image(image_file):
    img = Image.open(image_file)
    return pytesseract.image_to_string(img)

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
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
