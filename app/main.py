from pathlib import Path
from fastapi import FastAPI

from app.schemas import CustomerInput, PredictionResponse
from app.services.prediction import predict_churn
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import feedback

app = FastAPI(
    title="ChurnGuard AI",
    description="Customer churn prediction API",
    version="1.0.0",
)

app.include_router(feedback.router)

PROJECT_ROOT = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=PROJECT_ROOT / "static"),
    name="static"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to ChurnGuard AI",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput):
    return predict_churn(customer.model_dump())

@app.get("/dashboard")
def dashboard():
    return FileResponse(PROJECT_ROOT / "templates" / "index.html")