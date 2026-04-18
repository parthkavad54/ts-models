import pytest
from risk_engine.services.risk_calculator import (
    calculate_attendance_risk,
    calculate_marks_risk,
    calculate_assignment_risk,
    calculate_lms_risk,
    compute_overall_risk
)
from risk_engine.services.trend_detector import detect_trend
from risk_engine.services.simulation import simulate_risk
from risk_engine.models.academic_data import AcademicData

def test_attendance_risk():
    assert calculate_attendance_risk(75, 100) == 0.0
    assert calculate_attendance_risk(0, 100) == 100.0
    assert calculate_attendance_risk(37.5, 100) == 50.0

def test_marks_risk():
    assert calculate_marks_risk(50) == 0.0
    assert calculate_marks_risk(0) == 100.0
    assert calculate_marks_risk(100) == 0.0

def test_lms_risk():
    assert calculate_lms_risk(5) == 0.0
    assert calculate_lms_risk(0) == 100.0

def test_weighted_formula():
    records = [
        AcademicData(
            student_id="123", subject_id="s1", attendance=37.5, totalClasses=100,
            internalMarks=25, assignmentsPending=5, assignmentsTotal=10, lmsLoginsPerWeek=2.5
        )
    ]
    res = compute_overall_risk(records)
    assert res["score"] == 50.0
    assert res["level"] == "Medium"
    
def test_trend_detector():
    assert detect_trend([10, 20, 30]) == "Stable"
    assert detect_trend([10, 20, 30, 40]) == "Consistently Declining"
    assert detect_trend([10, 20, 30, 40, 50]) == "Consistently Declining"

def test_simulation_delta():
    records = [
        AcademicData(
            student_id="123", subject_id="s1", attendance=0, totalClasses=100,
            internalMarks=0, assignmentsPending=1, assignmentsTotal=1, lmsLoginsPerWeek=0
        )
    ]
    hypothetical = {
      "attendancePercentage": 100,
      "assignmentsPending": 0,
      "marksImprovement": 50,
      "lmsLoginsPerWeek": 5
    }
    
    res = simulate_risk(records, hypothetical)
    assert res["currentScore"] == 100.0
    assert res["projectedScore"] == 0.0
    assert res["delta"] == -100.0
