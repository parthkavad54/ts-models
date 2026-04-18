from pydantic import BaseModel
from datetime import datetime

class AlertCreate(BaseModel):
    student_id: str
    alert_type: str
    message: str

class Alert(AlertCreate):
    is_read: bool = False
    created_at: datetime
