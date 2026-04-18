from risk_engine.models.academic_data import AcademicData
from risk_engine.services.risk_calculator import compute_overall_risk

def simulate_risk(current_records: list[AcademicData], hypothetical: dict) -> dict:
    current_metrics = compute_overall_risk(current_records)
    
    proj_records = []
    for r in current_records:
        r_dict = r.dict()
        
        if "attendancePercentage" in hypothetical:
            r_dict["attendance"] = hypothetical["attendancePercentage"]
            r_dict["totalClasses"] = 100
        
        if "assignmentsPending" in hypothetical:
            r_dict["assignmentsPending"] = hypothetical["assignmentsPending"]
            
        if "marksImprovement" in hypothetical:
            r_dict["internalMarks"] += hypothetical["marksImprovement"]
            
        if "lmsLoginsPerWeek" in hypothetical:
            r_dict["lmsLoginsPerWeek"] = hypothetical["lmsLoginsPerWeek"]
            
        proj_records.append(AcademicData(**r_dict))
        
    proj_metrics = compute_overall_risk(proj_records)
    
    delta = round(proj_metrics["score"] - current_metrics["score"], 2)
    
    improvements = {
        "attendance": round(current_metrics["attendanceRisk"] - proj_metrics["attendanceRisk"], 2),
        "marks": round(current_metrics["marksRisk"] - proj_metrics["marksRisk"], 2),
        "assignments": round(current_metrics["assignmentRisk"] - proj_metrics["assignmentRisk"], 2),
        "lms": round(current_metrics["lmsRisk"] - proj_metrics["lmsRisk"], 2)
    }
    
    return {
        "currentScore": current_metrics["score"],
        "projectedScore": proj_metrics["score"],
        "delta": delta,
        "improvements": improvements
    }
