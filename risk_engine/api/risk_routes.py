from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timezone
from risk_engine.db.connection import get_collection
from risk_engine.models.academic_data import AcademicData
from risk_engine.services.risk_calculator import compute_overall_risk
from risk_engine.services.trend_detector import detect_trend
from risk_engine.services.cache_service import get_cached_risk_score, set_cached_risk_score, invalidate_cache
from risk_engine.services.simulation import simulate_risk
from risk_engine.services.ml_service import generate_ml_prediction
from pydantic import BaseModel

router = APIRouter(prefix="/api/risk", tags=["Risk"])

class SimulationRequest(BaseModel):
    student_id: str
    hypothetical: dict

class DirectPredictionRequest(BaseModel):
    attendance: float
    marks: float
    assignment: float
    lms: float

@router.post("/predict")
async def point_prediction(req: DirectPredictionRequest):
    import pandas as pd
    from risk_engine.services.ml_service import model
    if not model:
        raise HTTPException(status_code=500, detail="ML model offline")
    
    df = pd.DataFrame([{
        "attendance": req.attendance,
        "marks": req.marks,
        "assignment": req.assignment,
        "lms": req.lms
    }])
    pred = model.predict(df)[0]
    return {"ml_prediction": pred}

@router.post("/calculate/{student_id}")
async def calculate_risk(student_id: str):
    academic_col = get_collection("AcademicData")
    risk_col = get_collection("RiskScore")
    
    cursor = academic_col.find({"student_id": student_id})
    records_dict = await cursor.to_list(length=None)
    records = [AcademicData(**r) for r in records_dict]
    
    if not records:
        raise HTTPException(status_code=404, detail="No academic data found for student")
        
    metrics = compute_overall_risk(records)
    
    hist_cursor = risk_col.find({"student_id": student_id}).sort("calculatedAt", 1)
    hist_docs = await hist_cursor.to_list(length=None)
    hist_scores = [doc["score"] for doc in hist_docs]
    
    hist_scores.append(metrics["score"])
    
    trend = detect_trend(hist_scores)
    
    # Generate True ML Prediction
    ml_prediction = generate_ml_prediction(records)
    
    calculated_at = datetime.now(timezone.utc)
    
    risk_data = {
        "student_id": student_id,
        "studentId": student_id,
        "score": metrics["score"],
        "level": metrics["level"],
        "ml_prediction": ml_prediction,
        "attendanceRisk": metrics["attendanceRisk"],
        "marksRisk": metrics["marksRisk"],
        "assignmentRisk": metrics["assignmentRisk"],
        "lmsRisk": metrics["lmsRisk"],
        "trendFlag": trend,
        "calculatedAt": calculated_at
    }
    
    await risk_col.insert_one(risk_data.copy())
    
    if "_id" in risk_data:
        del risk_data["_id"]
        
    invalidate_cache(student_id)
    
    risk_data["calculatedAt"] = risk_data["calculatedAt"].isoformat()
    
    return {
        "studentId": risk_data["studentId"],
        "score": risk_data["score"],
        "level": risk_data["level"],
        "ml_prediction": risk_data["ml_prediction"],
        "attendanceRisk": risk_data["attendanceRisk"],
        "marksRisk": risk_data["marksRisk"],
        "assignmentRisk": risk_data["assignmentRisk"],
        "lmsRisk": risk_data["lmsRisk"],
        "trendFlag": risk_data["trendFlag"],
        "calculatedAt": risk_data["calculatedAt"].replace("+00:00", "Z")
    }

@router.get("/{student_id}")
async def get_risk(student_id: str):
    cached = get_cached_risk_score(student_id)
    if cached:
        return cached
        
    risk_col = get_collection("RiskScore")
    doc = await risk_col.find_one({"student_id": student_id}, sort=[("calculatedAt", -1)])
    
    if not doc:
        raise HTTPException(status_code=404, detail="Risk score not found")
        
    del doc["_id"]
    if "calculatedAt" in doc and hasattr(doc["calculatedAt"], "isoformat"):
        doc["calculatedAt"] = doc["calculatedAt"].isoformat().replace("+00:00", "Z")
        
    if "studentId" not in doc:
        doc["studentId"] = doc.get("student_id", student_id)
        
    set_cached_risk_score(student_id, doc)
    
    return doc

@router.get("/{student_id}/history")
async def get_risk_history(student_id: str):
    risk_col = get_collection("RiskScore")
    cursor = risk_col.find({"student_id": student_id}).sort("calculatedAt", 1)
    docs = await cursor.to_list(length=None)
    
    res = []
    for doc in docs:
        del doc["_id"]
        if "calculatedAt" in doc and hasattr(doc["calculatedAt"], "isoformat"):
            doc["calculatedAt"] = doc["calculatedAt"].isoformat().replace("+00:00", "Z")
        if "studentId" not in doc:
            doc["studentId"] = doc.get("student_id", student_id)
        res.append(doc)
    return res

@router.post("/simulate")
async def simulate(req: SimulationRequest):
    academic_col = get_collection("AcademicData")
    cursor = academic_col.find({"student_id": req.student_id})
    records_dict = await cursor.to_list(length=None)
    records = [AcademicData(**r) for r in records_dict]
    
    if not records:
        raise HTTPException(status_code=404, detail="No academic data found")
        
    result = simulate_risk(records, req.hypothetical)
    return result
