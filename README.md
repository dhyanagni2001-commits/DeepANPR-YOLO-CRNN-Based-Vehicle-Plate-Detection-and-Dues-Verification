# 🚀 DeepANPR: YOLO-Based License Plate Detection and OCR (FastAPI + Docker)

DeepANPR is a modular ANPR system that combines YOLO plate detection with OCR, implemented using FastAPI microservices.


It performs:

🔍 License plate detection (YOLOv8)

🔠 OCR text extraction (Tesseract)

💰 Pending dues verification

🔗 Gateway orchestration service

Each service runs independently and communicates through HTTP APIs.

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
