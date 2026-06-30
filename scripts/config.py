from typing import List

from pydantic import BaseModel


class Config(BaseModel):

    CAT_FEATURES: List[str] = ["Contract", "PaymentMethod", "InternetService", "MultipleLines", 'Partner', 'Dependents',
                    'PaperlessBilling', 'gender', 'has_services']
    TO_DROP: List[str] = ['customerID', 'TotalCharges']

    ALL_FEATURES: List[str] = [
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'MonthlyCharges', 'tenure',
        'Contract', 'PaymentMethod', 'InternetService',
        'MultipleLines', 'Partner', 'Dependents', 'PaperlessBilling',
        'gender', 'customerID', 'TotalCharges'
    ]

    INTERNET_SERVICES: List[str] = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                                    'StreamingMovies']

    STUDY_NAME: str = "CatBoost-model"
    MODEL_NAME: str = "CatBoost-model"

    THRESHOLD: float = 0.6

    RANDOM_SEED: int = 42
    THREADS_COUNT: int = 1
    LEARNING_RATE: float = 0.001
    BAGGING_TEMPERATURE: float = 1.0
    MODEL_ITERATIONS: int = 100
    DEPTH: int = 5
    VERBOSE: bool = False
    AUTO_CLASS_WEIGHTS: str = "Balanced"
    RANDOM_STRENGTH: float = 0.01
    L2_LEAF: int = 4

config = Config()