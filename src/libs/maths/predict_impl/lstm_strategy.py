from libs.maths.maths_interface import Predict_Interface
from libs.maths.market_window import MarketWindow
from conf.broker.broker_config import BrokerConfig
from conf.maths.maths_config import MathsConfig
from libs.log_manager.logger_factory import LoggerFactory

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

import joblib

class LSTM_Strategy(Predict_Interface):
    def __init__(self, logger_service_who):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.maths_lstm)

        self.configuration = MathsConfig.load()
        self.broker_configuration = BrokerConfig.load()
        self.scaler = MinMaxScaler(feature_range=(0,1))
        self.model = None
        self.seq_len = self.configuration.window_size_days
        
        persistence_dir = os.getenv("AINVEST_PERSISTENT_DIR", "")
        self.model_path = f"{persistence_dir}/lstm_model.h5"
        self.scaler_path = f"{persistence_dir}/lstm_scaler.pkl"

        self.model = load_model(self.model_path)
        self.scaler = joblib.load(self.scaler_path)

        self.callbacks = [
                EarlyStopping(monitor="loss", patience=5, restore_best_weights=True),
                ReduceLROnPlateau(monitor="loss", factor=0.5, patience=3)
            ]
    
    def predict(self, ticker: str, window: MarketWindow) -> float:
        prices = window.prices.values.reshape(-1, 1)

        if len(prices) < self.seq_len:
            self.log.warning("Not enough data for LSTM prediction", ticker)
            return 0.0

        cleaned = self._fix_outliers_iqr(prices)
        scaled = self.scaler.transform(cleaned)

        last_seq = scaled[-self.seq_len:].reshape(1, self.seq_len, 1)

        next_scaled = self.model.predict(last_seq, verbose=0)[0][0]
        next_price = self.scaler.inverse_transform([[next_scaled]])[0][0]

        latest_price = float(prices[-1][0])
        expected_return = (next_price / latest_price) - 1

        self.log.debug(f"LSTM expected return: {expected_return}", ticker)
        return expected_return
