DeepANPR – Automatic Number Plate Recognition (Microservices)

DeepANPR is a modular Automatic Number Plate Recognition (ANPR) system built using FastAPI with a microservices architecture.

It performs:

🔍 License plate detection (YOLOv8)

🔠 OCR text extraction (Tesseract)

💰 Pending dues verification

🔗 Gateway orchestration service

Each service runs independently and communicates through HTTP APIs.

🧩 System Architecture

Client → Gateway Service (8003)
             |
             v
     +-------------------+
     |  Detector Service | → YOLO → Plate Image Crop
     |        8000       |
     +-------------------+
             |
             v
     +-------------------+
     |    OCR Service    | → Extract Text
     |       8001        |
     +-------------------+
             |
             v
     +-------------------+
     |   Dues Service    | → Check pending dues
     |       8002        |
     +-------------------+

 🛠️ Tech Stack

    FastAPI

    Ultralytics YOLOv8

    Tesseract OCR

    Python 3.10+

    Docker

    NumPy

    Pydantic

    Requests

🧰 Prerequisites

    Python 3.10+

    Docker (optional but recommended)

    Tesseract installed (for OCR service)

    GPU optional (YOLO supports CPU)        
