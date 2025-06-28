from libs.maths.strategy_interface import Strategy_Interface

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

import numpy as np

class LSTM_Strategy(Strategy_Interface):
    def __init__(self, n_days_predict):
        self.scaler = MinMaxScaler()
        self.model: Sequential
        self.n_days_predict = n_days_predict
        self.x = []
        self.y = []

    # BRIEF: Convert raw sequential data into I/O pairs for training the model
    # seq_length: It slides a window of this length
    # RETURN: Two numpy arrays. Sequences of * seq_length (x) and the corresponding targets (number of sequences) (y) 
    def create_sequences(self, data, seq_length=60):
        self.x, self.y = [], []
        for i in range(seq_length, len(data)):
            self.x.append(data[i - seq_length:i])
            self.y.append(data[i])

        return np.array(self.x), np.array(self.y)

    def predict(self, data):
        n_data_days_fetched = len(data) - 1
        scaled_close_prices = self.scaler.fit_transform(data)

        self.x, self.y = self.create_sequences(scaled_close_prices, n_data_days_fetched)
        self.x = self.x.reshape(self.x.shape[0], self.x.shape[1], 1)

        self.model = Sequential([
            Input(shape=(n_data_days_fetched, 1)),
            LSTM(50, return_sequences=True),
            Dense(1)
        ])

        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(self.x, self.y, epochs=10, batch_size=16)

        last_seq = scaled_close_prices[-n_data_days_fetched:].reshape(1, n_data_days_fetched, 1)
        future_preds = []

        for _ in range(self.n_days_predict):
            next_scaled = self.model.predict(last_seq)[0][0]
            future_preds.append([next_scaled])
            last_seq = np.append(last_seq[:, 1:, :], [[next_scaled]], axis=1)

        future_prices = self.scaler.inverse_transform(np.array(future_preds).reshape(-1,1))
        for i, price in enumerate(future_prices, 1):
            print(f"Day {i}: ${price[0]:.2f}")
        

