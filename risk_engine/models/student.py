from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    student_id: str
    semester: int
    department: str
    mentor_id: Optional[str] = None
