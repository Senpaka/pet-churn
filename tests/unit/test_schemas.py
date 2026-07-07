import pytest
from pydantic import ValidationError

from services.fastapi.schemas import CustomerFeatures


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

def test_valid_customer_data():
    customer_data = valid_customer_data()

    customer = CustomerFeatures(**customer_data)

    assert customer.customerID == customer_data["customerID"]
    assert customer.gender == customer_data["gender"]

def test_invalid_customer_data():
    customer_data = valid_customer_data()
    customer_data["SeniorCitizen"] = 2

    with pytest.raises(ValidationError):
        CustomerFeatures(**customer_data)