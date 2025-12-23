from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI(title="DeepANPR – YOLO Plate Detector")

# Demo YOLO model
model = YOLO("yolov8n.pt")


def read_image(upload: UploadFile) -> np.ndarray:
    """
    Read uploaded image safely using PIL (no OpenCV dependency)
    """
    image_bytes = upload.file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return np.array(img)


@app.post("/detect")
async def detect_plate(file: UploadFile = File(...)):
    """
    Input: image
    Output:
      - found (bool)
      - bounding box
      - cropped plate image (hex-encoded JPG)
    """

    img = read_image(file)

    # Run YOLO inference
    results = model(img, verbose=False)[0]

    if results.boxes is None or len(results.boxes) == 0:
        return {"found": False}

    # Select highest confidence detection
    confs = results.boxes.conf.cpu().numpy()
    idx = int(np.argmax(confs))
    x1, y1, x2, y2 = results.boxes.xyxy[idx].cpu().numpy().astype(int)

    # Clamp to image bounds
    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w - 1, x2), min(h - 1, y2)

    if x2 <= x1 or y2 <= y1:
        return {"found": False}

    # Crop plate using NumPy
    plate_crop = img[y1:y2, x1:x2]

    # Encode cropped plate using PIL (not OpenCV)
    plate_image = Image.fromarray(plate_crop)
    buffer = io.BytesIO()
    plate_image.save(buffer, format="JPEG")

    return {
        "found": True,
        "confidence": float(confs[idx]),
        "box_xyxy": [int(x1), int(y1), int(x2), int(y2)],
        "plate_jpg_hex": buffer.getvalue().hex()
    }
