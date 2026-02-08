from libs.maths.base_trainer import BaseTrainer
from libs.maths.hybrid_feature_builder import HybridFeatureBuilder
from libs.maths.market_window import MarketWindow

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

class HybridEnsembleTraining(BaseTrainer):
    def __init__(self, tickers, lookback, horizon, output_dir, prices_dict, logger_service_type):
        # TODO: logging system
        super().__init__(tickers = tickers,
                         lookback = lookback,
                         horizon = horizon,
                         output_dir = output_dir,
                         prices_dict = prices_dict
                         )
        self.feature_builder = HybridFeatureBuilder()

    def build_sample(self, ticker, window, full_series, index):
        market_window = MarketWindow(
                ticker = ticker,
                prices = window,
                sentiment_score = None,
                timestamp = window.index[-1]
            )
        features = self.feature_builder.build(market_window)
        target = np.log(full_series.iloc[index + self.horizon] / full_series.iloc[index])
        return features.iloc[0], target

    def _train(self, splits):
        scaler = MinMaxScaler()

        X_train = pd.DataFrame(
            scaler.fit_transform(splits["X_train"]),
            columns=splits["X_train"].columns,
            index=splits["X_train"].index,
        )
        y_train = splits["y_train"]

        X_val = pd.DataFrame(
            scaler.transform(splits["X_val"]),
            columns=splits["X_val"].columns,
            index=splits["X_val"].index,
        )
        y_val = splits["y_val"]

        X_test = pd.DataFrame(
            scaler.transform(splits["X_test"]),
            columns=splits["X_test"].columns,
            index=splits["X_test"].index,
        )
        y_test = splits["y_test"]

        model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
        )

        model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )

        return model, {
            "scaler": scaler,
            "feature_schema": X_train.columns.tolist(),
            "test_data": {
                "X_test": X_test,
                "y_test": y_test,
            },
        }

