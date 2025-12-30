🚗 DeepANPR – Automatic Number Plate Recognition Microservices

DeepANPR is a modular Automatic Number Plate Recognition (ANPR) system built using FastAPI and a microservices architecture. It performs:

🔍 License plate detection (YOLOv8)

🔠 OCR extraction (Tesseract)

💰 Dues/penalty verification

🔗 Gateway orchestration service

Each component runs independently (Docker-ready), enabling scalability and easy replacement of individual components.

🧩 Architecture Overview
          +------------------+
          |   Gateway API    |
          |  (port 8003)     |
          +--------+---------+
                   |
                   v
     +-------------+--------------+
     |                            |
+----+----+                +------+------+
| Detector |                |    OCR     |
| 8000     |                |   8001     |
+----+----+                +------+------+
     |                            |
     v                            v
  Cropped Plate Image        Extracted Text
                \               /
                 \             /
                  v           v
                 +-------------+
                 |    Dues     |
                 |    8002     |
                 +-------------+

🛠️ Tech Stack

FastAPI

YOLOv8 (Ultralytics)

Tesseract OCR

Python 3.10+

Docker (containerized services)

Pydantic

Requests

📦 Services Included
Service	Description	Default Port
detector_service	Detects number plate using YOLO	8000
ocr_service	Extracts plate text using Tesseract OCR	8001
dues_service	Checks dues for recognized plate	8002
gateway_service	Main entrypoint orchestrator	8003
🧰 Prerequisites

Python 3.10+

pip

Docker & Docker Compose installed

Tesseract installed on OCR container or host

🐳 Run Using Docker (Recommended)

Each service already has Dockerfile.

Build images:

docker build -t detector_service ./detector_service
docker build -t ocr_service ./ocr_service
docker build -t dues_service ./dues_service
docker build -t gateway_service ./gateway_service


Run containers:

docker run -p 8000:8000 detector_service
docker run -p 8001:8001 ocr_service
docker run -p 8002:8002 dues_service
docker run -p 8003:8003 gateway_service


You may later add Docker Compose for orchestration

▶️ Run Locally Without Docker

Install dependencies:

pip install fastapi uvicorn ultralytics pillow pytesseract numpy requests


Run each service:

uvicorn detector_service:app --reload --port 8000
uvicorn ocr_service:app --reload --port 8001
uvicorn dues_service:app --reload --port 8002
uvicorn gateway_service:app --reload --port 8003

📍 API Endpoints
1️⃣ Detector Service (YOLO)

POST /detect

Input: image file

Output:

{
  "found": true,
  "confidence": 0.87,
  "box_xyxy": [12, 45, 250, 180],
  "plate_jpg_hex": "ffd8ffe0..."
}

2️⃣ OCR Service

POST /ocr

Input: image file

Output:

{
  "success": true,
  "text": "KA01AB1234"
}

3️⃣ Dues Service

POST /check_dues

Input:

{
  "plate_number": "KA01AB1234"
}


Output:

{
  "plate_number": "KA01AB1234",
  "found": true,
  "dues_pending": false,
  "amount": 0,
  "message": "No dues pending"
}

4️⃣ Gateway Service (Main Entry)

POST /process

Input: upload image file

Flow executed internally:

Detect plate

OCR recognition

Verify dues

Return full response

Output:

{
  "success": true,
  "plate_number": "KA05MN4321",
  "detector_confidence": 0.81,
  "bbox": [20, 50, 200, 140],
  "dues_result": {
    "found": true,
    "dues_pending": true,
    "amount": 500,
    "message": "Clear dues"
  }
}

🧪 Testing with cURL
curl -X POST -F "file=@car.jpg" http://localhost:8003/process

⚠️ Notes

YOLO model used: yolov8n.pt

Replace with custom ANPR-trained weights for better accuracy

OCR accuracy depends on:

crop quality

plate clarity

font & region

🚀 Future Enhancements

Docker-Compose orchestration

Kubernetes deployment

Full plate format validation (RTO regex)

Database backed dues service

Front-end dashboard