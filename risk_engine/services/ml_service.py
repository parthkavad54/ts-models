import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "risk_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: ML model not found or failed to load. {e}")
    model = None

def generate_ml_prediction(records):
    """
    Parses a list of AcademicData schemas back into the raw generic 
    features the Random Forest was trained on.
    """
    if not records or model is None:
        return "Unknown"
    
    avg_att = sum((r.attendance/r.totalClasses)*100 if r.totalClasses > 0 else 0 for r in records) / len(records)
    avg_marks = sum(r.internalMarks for r in records) / len(records)
    
    # Calculate % completion
    avg_assign = sum(((r.assignmentsTotal - r.assignmentsPending)/r.assignmentsTotal)*100 if r.assignmentsTotal > 0 else 0 for r in records) / len(records)
    
    # Scale weekly logins back to 0-100 logic
    avg_lms = sum((r.lmsLoginsPerWeek / 5.0) * 100.0 for r in records) / len(records)

    df = pd.DataFrame([{
        "attendance": avg_att,
        "marks": avg_marks,
        "assignment": avg_assign,
        "lms": avg_lms
    }])
    
    prediction = model.predict(df)[0]
    return prediction
