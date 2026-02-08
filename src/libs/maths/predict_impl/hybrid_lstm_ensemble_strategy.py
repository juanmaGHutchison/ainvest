from libs.maths.maths_interface import Predict_Interface
from libs.maths.strategy_impl.lstm_strategy import LSTM_Strategy
from libs.log_manager.logger_factory import LoggerFactory
from conf.maths.maths_config import MathsConfig

class FinalHybridStrategy(Predict_Interface):
    """
    Final production hybrid strategy:
    - LSTM for temporal dynamics
    - XGB ensemble for risk & regime
    - Confidence-weighted fusion
    """

    def __init__(self, logger_service_who):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.maths_lstm)

        self.configuration = MathsConfig.load()

        self.lstm = LSTM_Strategy(logger_service_who)
        self.hybrid_model = HybridEnsembleModel(logger_service_who)

        self.min_confidence = 0.6

    def predict(self, ticker: str, window: MarketWindow) -> float:
        # ---- LSTM signal ----
        lstm_return = self.lstm.predict(ticker, window)

        # ---- Hybrid signal ----
        features = HybridFeatureBuilder.build(window)
        if features is None:
            self.log.warning("Hybrid features unavailable", ticker)
            return 0.0

        hybrid_return = self.hybrid_model.predict(features)

        # ---- Confidence estimation ----
        downside_vol = features["downside_vol"].values[0] + 1e-6
        confidence = np.tanh(abs(hybrid_return) / downside_vol)

        if confidence < self.min_confidence:
            self.log.info(f"Low confidence ({confidence:.2f}). No trade.", ticker)
            return 0.0

        # ---- Fusion ----
        final_return = (
            0.6 * hybrid_return +
            0.4 * lstm_return
        )

        # ---- Risk filter ----
        expected_edge = final_return - 0.5 * features["volatility"].values[0]
        if expected_edge <= 0:
            self.log.info("Negative risk-adjusted edge. No trade.", ticker)
            return 0.0

        self.log.info(
            f"Trade signal: return={final_return:.4f}, confidence={confidence:.2f}",
            ticker
        )

        return expected_edge
