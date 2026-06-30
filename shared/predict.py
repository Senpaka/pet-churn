import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

from shared.features import FeatureBuilder


class Predictor:

    def __init__(self, model: CatBoostClassifier, threshold: float = 0.5):
        self.model = model
        self.feature_builder = FeatureBuilder()
        self.threshold = threshold

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        prediction = self.predict_proba(X)
        return (prediction >= self.threshold).astype(int)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        X = self.feature_builder.build(X)
        return self.model.predict_proba(X)[:, 1]
