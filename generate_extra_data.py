import pandas as pd
import numpy as np

def score_and_label(att, mk, ass, lm):
    # Clamping function
    cl = lambda v: max(0.0, min(100.0, v))
    
    att_risk = cl(((75.0 - att) / 75.0) * 100.0)
    mark_risk = cl(((50.0 - mk) / 50.0) * 100.0)
    # Using inverse correlation mapped from earlier datasets for assignment and lms
    assign_risk = cl(100 - ass) 
    lms_risk = cl(100 - lm)
    
    score = (0.40 * att_risk) + (0.30 * mark_risk) + (0.20 * assign_risk) + (0.10 * lms_risk)
    
    if score <= 45: label = "Low"
    elif score <= 65: label = "Medium"
    else: label = "High"
    
    return round(score, 2), label

def main():
    print("Loading original dataset to map bounds...")
    orig_path = "c:/Users/HELLO/Desktop/MODEL/TS-PS12.csv"
    orig_df = pd.read_csv(orig_path)
    
    last_id = orig_df['student_id'].max()
    num_rows = 25000
    
    print(f"Generating {num_rows} new fully synthetic parallel student records...")
    attendance = np.random.randint(30, 100, num_rows)
    marks = np.random.randint(20, 100, num_rows)
    assignment = np.random.randint(20, 100, num_rows)
    lms = np.random.randint(10, 100, num_rows)
    
    records = []
    for i in range(num_rows):
        sc, lbl = score_and_label(attendance[i], marks[i], assignment[i], lms[i])
        records.append({
            "student_id": last_id + i + 1,
            "attendance": attendance[i],
            "marks": marks[i],
            "assignment": assignment[i],
            "lms": lms[i],
            "risk_score": sc,
            "risk_label": lbl
        })
        
    extra_df = pd.DataFrame(records)
    
    combined = pd.concat([orig_df, extra_df], ignore_index=True)
    combined.to_csv(orig_path, index=False)
    
    print(f"Successfully injected! New massive dataset size: {combined.shape[0]} rows.")

if __name__ == "__main__":
    main()
