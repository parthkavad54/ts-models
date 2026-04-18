from typing import List
from risk_engine.models.academic_data import AcademicData

def clamp(value: float) -> float:
    return max(0.0, min(100.0, float(value)))

def calculate_attendance_risk(attendance: float, total_classes: float) -> float:
    if total_classes <= 0:
        return 0.0
    perc = (attendance / total_classes) * 100.0
    risk = ((75.0 - perc) / 75.0) * 100.0
    return clamp(risk)

def calculate_marks_risk(internal_marks: float) -> float:
    risk = ((50.0 - internal_marks) / 50.0) * 100.0
    return clamp(risk)

def calculate_assignment_risk(pending: float, total: float) -> float:
    if total <= 0:
        return 0.0
    risk = (pending / total) * 100.0
    return clamp(risk)

def calculate_lms_risk(logins_per_week: float) -> float:
    risk = ((5.0 - logins_per_week) / 5.0) * 100.0
    return clamp(risk)

def determine_level(score: float) -> str:
    if score <= 45.0:
        return "Low"
    elif score <= 65.0:
        return "Medium"
    else:
        return "High"

def compute_overall_risk(records: List[AcademicData]):
    if not records:
        return {
            "score": 0.0,
            "level": "Low",
            "attendanceRisk": 0.0,
            "marksRisk": 0.0,
            "assignmentRisk": 0.0,
            "lmsRisk": 0.0
        }
    
    att_risks = []
    mark_risks = []
    assgn_risks = []
    lms_risks = []
    
    for r in records:
        att_risks.append(calculate_attendance_risk(r.attendance, r.totalClasses))
        mark_risks.append(calculate_marks_risk(r.internalMarks))
        assgn_risks.append(calculate_assignment_risk(r.assignmentsPending, r.assignmentsTotal))
        lms_risks.append(calculate_lms_risk(r.lmsLoginsPerWeek))
        
    n = len(records)
    avg_att = sum(att_risks) / n
    avg_mark = sum(mark_risks) / n
    avg_assgn = sum(assgn_risks) / n
    avg_lms = sum(lms_risks) / n
    
    score = (0.40 * avg_att) + (0.30 * avg_mark) + (0.20 * avg_assgn) + (0.10 * avg_lms)
    
    return {
        "score": round(score, 2),
        "level": determine_level(score),
        "attendanceRisk": round(avg_att, 2),
        "marksRisk": round(avg_mark, 2),
        "assignmentRisk": round(avg_assgn, 2),
        "lmsRisk": round(avg_lms, 2)
    }
