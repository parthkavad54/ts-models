from pydantic import BaseModel
from datetime import datetime

class Assignment(BaseModel):
    subject_id: str
    title: str
    due_date: datetime
    max_marks: float
