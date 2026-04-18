from pydantic import BaseModel

class AcademicData(BaseModel):
    student_id: str
    subject_id: str
    attendance: float
    totalClasses: float
    internalMarks: float
    assignmentsPending: int
    assignmentsTotal: int
    lmsLoginsPerWeek: float
