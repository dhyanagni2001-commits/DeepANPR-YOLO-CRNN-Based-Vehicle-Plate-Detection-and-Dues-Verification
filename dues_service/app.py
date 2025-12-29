from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Dues Verification Service")

DUES_DB = {
    "KA01AB1234": 0,
    "KA05MN4321": 500,
    "TN09CD9999": 1200,
    "MH12XY7777": 0
}


class PlateRequest(BaseModel):
    plate_number: str


@app.get("/")
def health_check():
    return {"status": "dues service running"}


@app.post("/check_dues")
def check_dues(req: PlateRequest):
    plate = req.plate_number.upper().replace(" ", "")

    if plate not in DUES_DB:
        return {
            "plate_number": plate,
            "found": False,
            "message": "Vehicle not found in records"
        }

    amount = DUES_DB[plate]

    return {
        "plate_number": plate,
        "found": True,
        "dues_pending": amount > 0,
        "amount": amount,
        "message": "Clear dues" if amount > 0 else "No dues pending"
    }
