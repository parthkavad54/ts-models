from fastapi import APIRouter
from risk_engine.db.connection import get_collection

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("/at-risk")
async def get_at_risk_students():
    risk_col = get_collection("RiskScore")
    
    pipeline = [
        {"$sort": {"calculatedAt": -1}},
        {
            "$group": {
                "_id": "$student_id",
                "latestScore": {"$first": "$$ROOT"}
            }
        },
        {"$replaceRoot": {"newRoot": "$latestScore"}},
        {"$match": {"level": "High"}},
        {"$sort": {"score": -1}}
    ]
    
    cursor = risk_col.aggregate(pipeline)
    docs = await cursor.to_list(length=None)
    
    res = []
    for doc in docs:
        if "_id" in doc:
            del doc["_id"]
        if "calculatedAt" in doc and hasattr(doc["calculatedAt"], "isoformat"):
            doc["calculatedAt"] = doc["calculatedAt"].isoformat().replace("+00:00", "Z")
        if "studentId" not in doc:
            doc["studentId"] = doc.get("student_id")
        res.append(doc)
        
    return res
