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
    customerID: str = Field(..., description="The customer id")
    gender: str = Field(..., description="The gender of the customer")
    SeniorCitizen: int = Field(..., ge=0, le=1, description="Whether the customer is a senior citizen")
    Partner: str = Field(..., description="Whether the customer has a partner")
    Dependents: str = Field(..., description="Whether the customer has dependents")
    tenure: int = Field(..., ge=0, description="Number of months the customer has stayed")
    PhoneService: str = Field(..., description="Whether the customer has phone service")
    MultipleLines: str = Field(..., description="Whether the customer has multiple lines")
    InternetService: str = Field(..., description="Customer internet service type")
    OnlineSecurity: str = Field(..., description="Whether the customer has online security")
    OnlineBackup: str = Field(..., description="Whether the customer has online backup")
    DeviceProtection: str = Field(..., description="Whether the customer has device protection")
    TechSupport: str = Field(..., description="Whether the customer has tech support")
    StreamingTV: str = Field(..., description="Whether the customer has streaming TV")
    StreamingMovies: str = Field(..., description="Whether the customer has streaming movies")
    Contract: str = Field(..., description="The contract type")
    PaperlessBilling: str = Field(..., description="Whether the customer uses paperless billing")
    PaymentMethod: str = Field(..., description="The payment method")
    MonthlyCharges: float = Field(..., ge=0, description="The monthly charges")
    TotalCharges: float | None = Field(None, ge=0, description="The total charges")

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