from fastapi import FastAPI, File, UploadFile
import requests

app = FastAPI(title="ANPR Gateway Service")

# URLs of internal services
DETECTOR_URL = "http://localhost:8000/detect"
OCR_URL = "http://localhost:8001/ocr"
DUES_URL = "http://localhost:8002/check_dues"


@app.get("/")
def health():
    return {"status": "gateway running"}


@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    # ------------------------
    # 1) send image to detector
    # ------------------------
    files = {"file": (file.filename, await file.read(), file.content_type)}

    detector_response = requests.post(DETECTOR_URL, files=files).json()

    if not detector_response.get("found"):
        return {"success": False, "message": "No plate detected"}

    # get cropped plate image hex
    plate_hex = detector_response["plate_jpg_hex"]

    # ------------------------
    # 2) send crop hex to OCR
    # ------------------------
    ocr_response = requests.post(
        OCR_URL,
        json={"image_hex": plate_hex}
    ).json()

    if not ocr_response.get("success"):
        return {"success": False, "message": "OCR failed"}

    plate_number = ocr_response["plate_number"]

    # ------------------------
    # 3) send plate to dues service
    # ------------------------
    dues_response = requests.post(
        DUES_URL,
        json={"plate_number": plate_number}
    ).json()

    # ------------------------
    # 4) final combined response
    # ------------------------
    return {
        "success": True,
        "plate_number": plate_number,
        "dues_result": dues_response,
        "detector_confidence": detector_response["confidence"],
        "bbox": detector_response["box_xyxy"]
    }
