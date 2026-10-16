from typing import Literal

from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int = Field(ge=0, le=100)
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["Yes", "No", "No internet service"]
    OnlineBackup: Literal["Yes", "No", "No internet service"]
    DeviceProtection: Literal["Yes", "No", "No internet service"]
    TechSupport: Literal["Yes", "No", "No internet service"]
    StreamingTV: Literal["Yes", "No", "No internet service"]
    StreamingMovies: Literal["Yes", "No", "No internet service"]
    Contract: Literal[
        "Month-to-month",
        "One year",
        "Two year"
    ]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


class PredictionResponse(BaseModel):
    prediction: Literal["Churn", "No Churn"]
    churn_probability: float
    risk_level: Literal["Low", "Medium", "High"]

class FeedbackInput(BaseModel):
    prediction_id: str =Field(min_length=8, max_length=64)
    is_correct:bool
    customer_input: CustomerInput
    prediction : Literal["Churn","No Churn"]
    churn_probability:float=Field(ge=0,le=1)
    risk_level : Literal["Low","Medium","High"]

