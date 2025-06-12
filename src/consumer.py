#!/usr/bin/env python3

from libs.broker.broker_adapter import Broker_Adapter
from libs.queue.queue_adapter import Queue_Adapter

import json
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class Consumer:
    def __init__(self):
        self.broker = Broker_Adapter()
        self.queue_consumer = Queue_Adapter()

        self.broker.init_historic_api()
        self.queue_consumer.init_consumer()

    def create_sequences(self, data, seq_length=60):
        x, y = [], []
        for i in range(seq_length, len(data)):
            x.append(data[i - seq_length:i])
            y.append(data[i])
        return np.array(x), np.array(y)

    # TODO: refactor
    def consuming_action(self, message):
        print(f"Received: {message.value.decode('utf-8')}")
        message_json = json.loads(message.value.decode('utf-8'))
        ticker = message_json['ticker']

        prices = self.broker.get_data_from_stock(ticker).values.reshape(-1, 1)

        scaler = MinMaxScaler()
        scaled_close_prices = scaler.fit_transform(prices)

        x, y = self.create_sequences(scaled_close_prices, 60)
        x = x.reshape(x.shape[0], x.shape[1], 1)

        # TODO: Strategy pattern ?
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(60, 1)),
            LSTM(50),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x, y , epochs=10, batch_size=16)

        last_seq = scaled_close_prices[-60:].reshape(1, 60, 1)
        future_preds = []

        for _ in range(7):
            next_scaled = model.predict(last_seq)[0][0]
            future_preds.append([next_scaled])
            last_seq = np.append(last_seq[:, 1:, :], [[[next_scaled]]], axis=1)

        future_prices = scaler.inverse_transform(np.array(future_preds))
        for i, price in enumerate(future_prices, 1):
            print(f"Day {i}: ${price[0]:.2f}")
                
    def start_consumer(self):
        self.queue_consumer.start_consuming(self.consuming_action)

if __name__ == "__main__":
    consumer = Consumer()

    consumer.start_consumer()
