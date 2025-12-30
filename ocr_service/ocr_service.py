from fastapi import FastAPI, UploadFile, File
from PIL import Image
import pytesseract
import io

app = FastAPI(title="OCR Service")

@app.get("/")
def root():
    return {"status": "OCR API running"}

def read_image(upload: UploadFile) -> Image.Image:
    # Read uploaded file bytes
    image_bytes = upload.file.read()
    # Open in PIL
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return img

@app.post("/ocr")
async def do_ocr(file: UploadFile = File(...)):
    """
    Input: image file
    Output: extracted text
    """

    img = read_image(file)

    # Run OCR
    text = pytesseract.image_to_string(img)

    return {
        "success": True,
        "text": text.strip()
    }
