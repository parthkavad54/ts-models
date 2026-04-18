# EduGuard / AcadWatch Risk Engine

The Early Academic Risk Detection System backend is a FastAPI application designed to predict and track students who are academically at risk using a dynamically weighted linear risk score formula.

## Prerequisites

Before connecting to the backend, ensure you have the following installed and running on your system:
- **Python 3.9+**
- **MongoDB** (Local instance on port 27017 or a Cloud URI)
- **Redis** (Local instance on port 6379 or a Cloud URI)

## 1. Installation

First, navigate into the project directory and install the required Python dependencies:

```bash
cd risk_engine
pip install -r requirements.txt
```

## 2. Environment Variables

The backend relies on environment variables to connect to MongoDB and Redis. Create a `.env` file inside the `risk_engine` directory with the following variables:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=eduguard

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
```
*(Adjust the host and port values if your MongoDB or Redis instances are running somewhere else or require authentication).*

## 3. Running the Server

Start the FastAPI application using the Uvicorn ASGI server. From the root directory (the parent directory of `risk_engine`), run:

```bash
uvicorn risk_engine.main:app --reload
```

The backend server will start at: **http://127.0.0.1:8000**

You can also view the automatically generated interactive documentation from FastAPI by visiting: 
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 4. Connecting and Using the API

Here is an overview of the primary endpoints you can call from your frontend or Postman:

### Risk Calculation
Trigger the recalculation of the risk score for a specific student. This forces MongoDB to fetch all academic data, process the scores, update history trends, and invalidate the Redis cache.

- **POST** `/api/risk/calculate/{student_id}`
- **Response**:
```json
{
  "studentId": "123",
  "score": 68.5,
  "level": "High",
  "attendanceRisk": 40.2,
  "marksRisk": 89.5,
  "assignmentRisk": 60.3,
  "lmsRisk": 70.1,
  "trendFlag": "Consistently Declining",
  "calculatedAt": "2024-01-15T10:30:00Z"
}
```

### Get Risk Score
Fetch the most recent risk score. Responses are cached in Redis with a 1-hour TTL for incredibly fast retrieval.

- **GET** `/api/risk/{student_id}`

### Get Risk History
Fetch the historical dataset to populate trend graphs on the frontend.

- **GET** `/api/risk/{student_id}/history`

### What-If Simulation
Send hypothetical scenarios to see the immediate effect on a student's risk profile without persisting data to the database.

- **POST** `/api/risk/simulate`
- **Body**:
```json
{
  "student_id": "123",
  "hypothetical": {
    "attendancePercentage": 90,
    "assignmentsPending": 0,
    "marksImprovement": 15,
    "lmsLoginsPerWeek": 5
  }
}
```

### High-Risk Students List
Retrieve a descending list of all students currently marked with a "High" risk level.

- **GET** `/api/students/at-risk`

---

## 5. Running Tests
Pytest unit tests are included to cover the simulation logic, risk weights, edge cases, and trend algorithms. Note that you may need to add the project root to your Python path to execute seamlessly.

```bash
python -m pytest risk_engine/tests
```
