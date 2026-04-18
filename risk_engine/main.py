from fastapi import FastAPI
from risk_engine.api import risk_routes, student_routes, alert_routes

app = FastAPI(title="EduGuard / AcadWatch Risk Engine")

app.include_router(risk_routes.router)
app.include_router(student_routes.router)
app.include_router(alert_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to EduGuard Risk Engine API"}
