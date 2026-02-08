from libs.maths.maths_interface import Predict_Interface
from libs.log_manager.logger_factory import LoggerFactory
from libs.broker.broker_facade import Broker_Facade
from conf.maths.maths_config import MathsConfig

import pandas as pd
import joblib
import os

class HybridEnsembleStrategy(Predict_Interface):
    def __init__(self, logger_service_who):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.maths_lstm)

        persistence_dir = os.getenv("AINVEST_PERSISTENT_DIR", "")
        self.model = joblib.load(f"{persistence_dir}/hybrid_model.pkl")
        self.scaler = joblib.load(f"{persistence_dir}/hybrid_scaler.pkl")

    def predict(self, features: pd.DataFrame) -> float:
        scaled = pd.DataFrame(
            self.scaler.transform(features),
            columns=features.columns
        )
        return float(self.model.predict(scaled)[0])

    def get_strategy_name(self):
        return self.configuration.strategy_used

