from fastapi import APIRouter
from datetime import datetime, timezone
from risk_engine.db.connection import get_collection
from risk_engine.models.alert import AlertCreate

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.post("/create")
async def create_alert(alert: AlertCreate):
    alert_col = get_collection("Alert")
    doc = alert.dict()
    doc["is_read"] = False
    doc["created_at"] = datetime.now(timezone.utc)
    
    result = await alert_col.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    doc["created_at"] = doc["created_at"].isoformat().replace("+00:00", "Z")
    return doc

@router.get("/{student_id}")
async def get_alerts(student_id: str):
    alert_col = get_collection("Alert")
    cursor = alert_col.find({"student_id": student_id, "is_read": False})
    docs = await cursor.to_list(length=None)
    res = []
    for doc in docs:
        doc["_id"] = str(doc["_id"])
        if "created_at" in doc and hasattr(doc["created_at"], "isoformat"):
            doc["created_at"] = doc["created_at"].isoformat().replace("+00:00", "Z")
        res.append(doc)
    return res
