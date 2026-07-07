import pandas as pd
import pytest

from shared.features import FeatureBuilder


def test_feature_build_without_churn():
    df = pd.DataFrame({
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
    }, index=[0])

    builder = FeatureBuilder()
    result = builder.build(df)

    assert "Has_internet" in result.columns
    assert "NumServices" in result.columns
    assert "has_services" in result.columns
    assert "customerID" not in result.columns
    assert "TotalCharges" not in result.columns

def test_error_feature_builder():
    df = pd.DataFrame({
        "customerID": "7590-VHVEG",
        "gender": "Female"
    }, index=[0])

    builder = FeatureBuilder()

    with pytest.raises(ValueError):
        builder.build(df)

