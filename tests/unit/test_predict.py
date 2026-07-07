import numpy as np
import pandas as pd

from shared.predict import Predictor


class FakeModel:

    def predict_proba(self, X):
        return np.array([
            [0.2, 0.8],
            [0.7, 0.3],
        ])

class FakeFeatureBuilder:

    def build(self, X):
        return X


def test_predictor_to_return_positive_class():
    df = pd.DataFrame([
        {"x": 1},
        {"x": 2},
    ])

    predictor = Predictor(
        FakeModel(),
        FakeFeatureBuilder(),
        0.6
    )

    proba = predictor.predict_proba(df)

    assert proba.shape == (2,)
    assert proba.tolist() == [0.8, 0.3]

def test_threshold_in_prediction():
    df = pd.DataFrame([
        {"x": 1},
        {"x": 2},
    ])

    predictor = Predictor(
        FakeModel(),
        FakeFeatureBuilder(),
        0.6
    )

    prediction = predictor.predict(df)

    assert prediction.tolist() == [1, 0]