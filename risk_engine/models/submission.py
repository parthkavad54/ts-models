from pydantic import BaseModel
from datetime import datetime

class Submission(BaseModel):
    assignment_id: str
    student_id: str
    submitted_at: datetime
    marks_obtained: float
