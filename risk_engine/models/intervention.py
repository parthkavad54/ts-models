from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Intervention(BaseModel):
    student_id: str
    mentor_id: str
    notes: str
    intervention_type: str
    date: datetime
    effectiveness_score: Optional[float] = None
