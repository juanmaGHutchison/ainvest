from libs.maths.maths_interface import Predict_Interface
from libs.maths.market_window import MarketWindow
from libs.log_manager.logger_factory import LoggerFactory
from conf.maths.maths_config import MathsConfig

from pathlib import Path

import os
import json
import joblib
import numpy as np

from keras.models import load_model


class LSTM_Strategy(Predict_Interface):

    def __init__(self, logger_service_type, training_dir):
        self.log = LoggerFactory(logger_service_type)
        self.log.init_logger(self.log.maths_lstm)

        self.configuration = MathsConfig.load()

        strategy_cache_dir = Path(training_dir)

        # ✅ cargar modelo
        self.model = load_model(f"{strategy_cache_dir}/model.keras")

        # ✅ cargar scaler
        self.scaler = joblib.load(f"{strategy_cache_dir}/scaler.pkl")

        # metadata (opcional)
        with open(os.path.join(strategy_cache_dir, "training_meta.json")) as f:
            self.meta = json.load(f)

        self.lookback = self.meta["lookback"]

    # --------------------------------------------------
    def get_strategy_name(self):
        return "LSTM"

    # --------------------------------------------------
    def predict(self, market_window: MarketWindow) -> float:

        prices = market_window.prices
        ticker = market_window.ticker

        if prices is None or len(prices) < self.lookback + 1:
            self.log.warning("Not enough data for LSTM", ticker)
            return 0.0

        try:
            # Ventana de precios
            window_prices = prices.iloc[-(self.lookback + 1):].values

            # Convert to returns (log-returns)
            returns = np.log(window_prices[1:] / window_prices[:-1])

            # Reshape for LSTM → (1, lookback, 1)
            X = returns.reshape(1, self.lookback, 1)

            # Predicción log-return
            log_pred_return = self.model.predict(X, verbose=0)[0][0]

            # 🔹 Convert log-return → linear return
            predicted_return = np.expm1(log_pred_return)  # e^(log-return) - 1

            predicted_return = float(predicted_return)

            # 🚫 evitar ruido
            if abs(predicted_return) < 0.01:
                self.log.info(f"Signal too weak ({predicted_return:.4f})", ticker)
                return 0.0

            # 🚫 limitar extremo
            predicted_return = np.clip(predicted_return, -0.2, 0.2)

            self.log.info(f"LSTM return={predicted_return:.4f}", ticker)

            return predicted_return

        except Exception as e:
            self.log.error(f"LSTM prediction failed: {e}", ticker)
            return 0.0
