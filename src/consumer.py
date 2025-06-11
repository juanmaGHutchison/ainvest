#!/usr/bin/env python3

# TODO: Use
# from libs.broker.broker_news_adapter import Broker_News_Adapter
# TODO: move to broker adapter. Maybe do an adapter for historical
from alpaca.data import StockHistoricalDataClient, StockTradesRequest

from kafka import KafkaConsumer

from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_sequences(data, seq_length=60):
    x, y = [], []
    for i in range(seq_length, len(data)):
        x.append(data[i - seq_length:i])
        y.append(data[i])
    return np.array(x), np.array(y)

if __name__ == "__main__":
    load_dotenv("config/alpaca.env")
    load_dotenv("config/kafka.env")

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    KAFKA_SERVER = f"{os.getenv('KAFKA_DOCKER_NAME')}:{os.getenv('KAFKA_PORT')}"
    TOPIC = os.getenv("MAIN_TOPIC")

    consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_SERVER,
            group_id = 'consumer-1',
            auto_offset_reset = 'earliest'
            )

    broker_historic = StockHistoricalDataClient(API_KEY, API_SECRET)
    yesterday = datetime.today() - timedelta(days=1)

    # TODO: kafka adapter
    consumer.subscribe([TOPIC])

    for message in consumer:
        print(f"Received: {message.value.decode('utf-8')}")
        message_json = json.loads(message.value.decode('utf-8'))
        ticker = message_json['ticker']

                # start = yesterday - timedelta(days=120),
        historic_data_params = StockTradesRequest(
                symbol_or_symbols = ticker,
                start = yesterday - timedelta(days=4),
                end = yesterday
                )
        trades = broker_historic.get_stock_trades(historic_data_params)
        trade_list = trades[ticker]

        dataframe = pd.DataFrame([{
            'timestamp': trades[ticker][i].timestamp,
            'price': trades[ticker][i].price,
            'size': trades[ticker][i].size
            } for i in range(len(trade_list))
        ])

        dataframe.set_index('timestamp', inplace = True)
        dataframe.sort_index(inplace = True)
        close_prices = dataframe['price'].values.reshape(-1, 1)
        scaler = MinMaxScaler()
        scaled_close_prices = scaler.fit_transform(close_prices)

        x, y = create_sequences(scaled_close_prices, 60)
        x = x.reshape(x.shape[0], x.shape[1], 1)

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
