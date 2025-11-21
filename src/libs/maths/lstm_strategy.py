from libs.maths.strategy_interface import Strategy_Interface
from conf.broker.broker_config import BrokerConfig
from conf.maths.maths_config import MathsConfig

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

import numpy as np

class LSTM_Strategy(Strategy_Interface):
    def __init__(self):
        self.configuration = MathsConfig.load()
        self.broker_configuration = BrokerConfig.load()
        self.scaler = MinMaxScaler(feature_range=(0,1))
        self.model = None
        self.seq_len = self.configuration.window_size_days

    def _create_sequences(self, data):
        x, y = [], []
        for i in range(self.seq_len, len(data)):
            x.append(data[i - self.seq_len:i])
            y.append(data[i])

        return np.array(x), np.array(y)

    def _train(self, data):
        scaled = self.scaler.fit_transform(data)
        # TODO what is seq_len
        x, y = self._create_sequences(scaled)
        x = x.reshape((x.shape[0], x.shape[1], 1))

        self.model = Sequential([
            Input(shape=(self.seq_len, 1)),
            LSTM(64, return_sequences=False),
                 Dense(1)
            ])

        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(x, y, epochs=50, batch_size=32, verbose=0)

    def predict(self, data):
        self._train(data)

        scaled = self.scaler.transform(data)
        last_seq = scaled[-self.seq_len:].reshape(1, self.seq_len, 1)
        preds = []

        for _ in range(self.broker_configuration.historic_lookback_days):
            next_scaled = self.model.predict(last_seq, verbose=0)[0][0]
            preds.append(next_scaled)
            last_seq = np.append(last_seq[:, 1:, :], [[[next_scaled]]], axis=1)

        return self.scaler.inverse_transform(np.array(preds).reshape(-1, 1))

    def get_max_prediction(self, data):
        return float(np.max(data))

