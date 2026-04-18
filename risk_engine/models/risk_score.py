from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RiskScore(BaseModel):
    student_id: str = Field(alias="studentId")
    score: float
    level: str
    ml_prediction: Optional[str] = None
    attendanceRisk: float
    marksRisk: float
    assignmentRisk: float
    lmsRisk: float
    trendFlag: str
    calculatedAt: datetime

    class Config:
        populate_by_name = True
