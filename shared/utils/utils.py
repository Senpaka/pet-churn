def get_risk_level(probability: float) -> str:

    if probability > 0.9:
        return "Critical"
    elif probability > 0.8:
        return "High"
    elif probability > 0.6:
        return "Medium"

    return "Low"