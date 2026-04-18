from pydantic import BaseModel

class Subject(BaseModel):
    name: str
    semester: int
    syllabus: str
