import numpy as np
import pandas as pd

from fastapi.testclient import TestClient
from services.fastapi.app import app


class FakePredictor:
    threshold = 0.6

    def predict_proba(self, df):
        return np.array([0.8])

def valid_customer_data():
    return {
        "customerID": "7590-VHVEG",
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
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85,
        "TotalCharges": 29.85,
    }

def test_predict_endpoint_response():
    app.state.predictor = FakePredictor()

    client = TestClient(app)
    response = client.post("/model/predict", json=valid_customer_data())

    assert response.status_code == 200

    data = response.json()

    print(data)

    assert data["customer_id"] == "7590-VHVEG"
    assert data["prediction"] == "Churn"
    assert data["probability"] == 0.8