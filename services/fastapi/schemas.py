from typing import List

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class HealthResponse(BaseModel):
    status: int
    timestamp: datetime

class DataBaseResponse(BaseModel):
    status: str
    timestamp: datetime

class CustomerFeatures(BaseModel):
    customerID: int = Field(..., ge=0, description="The customer id")
    gender: str = Field(..., description="The gender of the user (male/female)")
    SeniorCitizen: int = Field(..., description="The SeniorCitizen")
    Partner: str = Field(..., description="The Partner")
    Dependents: str = Field(..., description="The Dependents")
    tenure: int = Field(..., description="The tenure")
    PhoneService: str = Field(..., description="The Phone Service")
    MultipleLines: str = Field(..., description="The MultipleLines")
    InternetService: str = Field(..., description="The Internet Service")
    OnlineSecurity: str = Field(..., description="The OnlineSecurity")
    OnlineBackup: str = Field(..., description="The OnlineBackup")
    DeviceProtection: str = Field(..., description="The DeviceProtection")
    TechSupport: str = Field(..., description="The TechSupport")
    StreamingTV: str = Field(..., description="The StreamingTV")
    StreamingMovies: str = Field(..., description="The StreamingMovies")
    Contract: str = Field(..., description="The Contract")
    PaperlessBilling: str = Field(..., description="The PaperlessBilling (Yes/No)")
    PaymentMethod: str = Field(..., description="The PaymentMethod")
    MonthlyCharges: int = Field(..., ge=0, description="The MonthlyCharges")
    TotalCharges: int = Field(..., ge=0, description="The TotalCharges")

class PredictionResponse(BaseModel):
    customer_id: int
    prediction: str
    probability: float = Field(..., ge=0, le=1 ,description="The probability of the customer")
    risk: str
    timestamp: datetime

    @field_validator("prediction", mode="before")
    @classmethod
    def prediction_validator(cls, prediction: str) -> str:
        if prediction not in ["Churn", "Stay"]:
            raise ValueError("Предсказание должно быть либо Churn либо Stay")
        return prediction

    @field_validator("risk", mode="before")
    @classmethod
    def risk_validator(cls, risk: str) -> str:
        if risk not in ["High", "Medium", "Low", "Critical"]:
            raise ValueError("Риск должен быть в списке значений [High, Medium, Low, Critical]")
        return risk

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "customerID": 7590,
                "gender": "Female",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 1,
                "PhoneService": "No",
                "MultipleLines": "No phone service",
                "InternetService": "DSL",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "No",
                "StreamingMovies": "No",
                "Contract": "Month-to-month",
                'PaperlessBilling': 'Yes',
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 29,
                "TotalCharges": 29
            }
        }
    )

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]