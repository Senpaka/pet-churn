import numpy as np
import pandas as pd
from scripts.config import config

import logging

logger = logging.getLogger(__name__)

_to_drop = config.TO_DROP
_features = config.ALL_FEATURES

class FeatureBuilder:

    def __init__(self):
        pass

    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if not set(_features).issubset(set(df.columns)):
            logger.warning(f"Не все фичи присутствуют в датасете. Отсутствуют{set(_features) - set(df.columns)}")
            raise ValueError("Не все фичи присутствуют в датасете!")

        df.drop(_to_drop, axis=1, inplace=True)

        df['Has_internet'] = (df['InternetService'] != 'No').astype(int)
        df['PhoneService'] = (df['PhoneService'] == 'Yes').astype(int)

        internet_services = config.INTERNET_SERVICES

        df['NumServices'] = 0

        for service in internet_services:
            df[service] = (df[service] == 'Yes').astype(int)
            df['NumServices'] += df[service]

        df['has_services'] = np.where(df['NumServices'] != 0, 1, 0).astype(int)

        if 'Churn' in df.columns:
            df['Churn'] = np.where(df['Churn'] == 'Yes', 1, 0).astype(int)

        self._features_list = df.columns.to_list()

        logger.info(f"Созданы новые фичи. Итоговые фичи: {self._features_list}")

        return df