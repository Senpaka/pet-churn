import numpy as np
import pandas as pd

from scripts.config import config

import logging

logger = logging.getLogger(__name__)

_to_drop = config.TO_DROP
_features = config.ALL_FEATURES

class CreateFeature:

    def __init__(self):
        self._features_list = None

    def create_feature(self, df: pd.DataFrame) -> pd.DataFrame:

        df_train = df.copy()

        if not set(_features).issubset(set(df.columns)):
            logger.warning(f"Не все фичи присутствуют в датасете. Отсутствуют{set(_features) - set(df.columns)}")
            raise "Не все фичи присутствуют в датасете!"

        df_train.drop(_to_drop, axis=1, inplace=True)

        df_train['Has_internet'] = (df_train['InternetService'] != 'No').astype(int)
        df_train['PhoneService'] = (df_train['PhoneService'] == 'Yes').astype(int)

        internet_services = config.INTERNET_SERVICES

        df_train['NumServices'] = 0

        for service in internet_services:
            df_train[service] = (df_train[service] == 'Yes').astype(int)
            df_train['NumServices'] += df_train[service]

        df_train['has_services'] = np.where(df_train['NumServices'] != 0, 1, 0).astype(int)

        if 'Churn' in df_train.columns:
            df_train['Churn'] = np.where(df_train['Churn'] == 'Yes', 1, 0).astype(int)

        self._features_list = df_train.columns.to_list()

        logger.info(f"Созданы новые фичи. Итоговые фичи: {self._features_list}")

        return df_train
