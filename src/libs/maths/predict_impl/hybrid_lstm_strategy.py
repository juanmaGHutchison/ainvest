from libs.maths.maths_interface import Predict_Interface
from libs.maths.predict_impl.lstm_strategy import LSTM_Strategy
from libs.maths.predict_impl.hybrid_ensemble_strategy import HybridEnsembleStrategy
from libs.maths.market_window import MarketWindow
from libs.maths.hybrid_feature_builder import HybridFeatureBuilder
from conf.maths.maths_config import MathsConfig

from libs.log_manager.logger_factory import LoggerFactory

import numpy as np

class HybridLSTMStrategy(Predict_Interface):
    """
    Final production hybrid strategy:
    - LSTM for temporal dynamics
    - XGB ensemble for risk & regime
    - Confidence-weighted fusion
    """

    def __init__(self, logger_service_who, strategy_dir):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.maths_lstm)

        self.configuration = MathsConfig.load()

        self.lstm_component = LSTM_Strategy(logger_service_who, strategy_dir)
        self.hybrid_component = HybridEnsembleStrategy(logger_service_who, strategy_dir)

        self.min_confidence = 0.6

    def predict(self, window: MarketWindow) -> float:
        lstm_return = self.lstm_component.predict(window)
        hybrid_return = self.hybrid_component.predict(window)

        features = self.hybrid_component.feature_builder.build(window)

        if features is None or features.empty:
            self.log.warning(f"Feature building failed. TODO: Improve log")

        # ---- Confidence estimation ----
        downside_vol = features["downside_vol"].values[0] + 1e-6
        confidence = np.tanh(abs(hybrid_return) / downside_vol)

        if confidence < self.min_confidence:
            self.log.info(f"Low confidence ({confidence:.2f}). No trade.")
            return 0.0

        # ---- Fusion ----
        final_return = (
            0.6 * hybrid_return +
            0.4 * lstm_return
        )

        # ---- Risk filter ----
        expected_edge = features["volatility"].values[0] - (final_return * 0.5)
        if expected_edge <= 0:
            self.log.info("Negative risk-adjusted edge. No trade.")
            return 0.0

        self.log.info(
            f"Trade signal: return={final_return:.4f}, confidence={confidence:.2f}")

        return expected_edge
