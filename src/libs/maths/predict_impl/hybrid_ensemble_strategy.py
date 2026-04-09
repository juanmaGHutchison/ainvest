from libs.maths.maths_interface import Predict_Interface
from libs.maths.market_window import MarketWindow
from libs.maths.hybrid_feature_builder import HybridFeatureBuilder
from libs.log_manager.logger_factory import LoggerFactory
from libs.broker.broker_facade import Broker_Facade
from conf.maths.maths_config import MathsConfig

from pathlib import Path

import joblib
import pickle
import os
import json

class HybridEnsembleStrategy(Predict_Interface):
    def __init__(self, logger_service_who, training_dir):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.maths_lstm)
        self.configuration = MathsConfig.load()

        strategy_cache_dir = Path(training_dir)
        for item in strategy_cache_dir.iterdir():
            self.log.info(item)

        # TODO: all pkl files shall be variables
        self.model = joblib.load(f"{strategy_cache_dir}/model.pkl")
        self.scaler = joblib.load(f"{strategy_cache_dir}/scaler.pkl")

        with open(os.path.join(strategy_cache_dir, "feature_schema.pkl"), "rb") as f:
            self.feature_schema = pickle.load(f)

        with open(os.path.join(strategy_cache_dir, "training_meta.json")) as f:
            self.meta = json.load(f)

        self.feature_builder = HybridFeatureBuilder()

    def predict(self, market_window: MarketWindow) -> float:
        features = self.feature_builder.build(market_window)
        if features is None:
            self.log.warning("No features built")
            return .0

        try:
            X = features[self.feature_schema]
        except KeyError as e:
            raise RuntimeError(f"Feature mismatch: {e}")

        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)[0]

    def get_strategy_name(self):
        return self.configuration.strategy_used

