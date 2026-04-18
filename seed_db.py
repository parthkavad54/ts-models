import asyncio
import pandas as pd
from risk_engine.db.connection import get_collection

async def seed_data():
    csv_path = "c:/Users/HELLO/Desktop/MODEL/TS-PS12.csv"
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    academic_col = get_collection("AcademicData")
    
    # Check if data already exists
    count = await academic_col.count_documents({})
    if count > 0:
        print("Database already contains data! To re-seed, drop the collection first.")
        return

    print("Formatting records for MongoDB...")
    records = []
    # We will pick the first 1000 to keep it incredibly fast, or all 50k. 
    # Let's seed all 50,000 using insert_many in batches
    for i, row in df.iterrows():
        # Extrapolate mapping from CSV out-of-100 metrics to the explicit schema variables
        record = {
            "student_id": str(row["student_id"]),
            "subject_id": "SUB101", # Assume all this data is for one core subject
            "attendance": float(row["attendance"]),
            "totalClasses": 100.0,
            "internalMarks": float(row["marks"]),
            # If CSV 'assignment' is a completion %, pending = 100 - completion
            "assignmentsPending": int(100 - row["assignment"]),
            "assignmentsTotal": 100,
            # If CSV 'lms' is an activity %, scale it back to 0-5 weekly scale
            "lmsLoginsPerWeek": float(row["lms"] / 100.0 * 5.0)
        }
        records.append(record)

    print("Inserting into MongoDB AcademicData collection...")
    # Insert in batches of 5000
    batch_size = 5000
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        await academic_col.insert_many(batch)
        print(f"Inserted batch {i//batch_size + 1}...")

    print("Successfully seeded all AcademicData!")

if __name__ == "__main__":
    asyncio.run(seed_data())
