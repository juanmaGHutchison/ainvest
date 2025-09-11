#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.maths.lstm_strategy import LSTM_Strategy

import json

class Consumer:
    def __init__(self):
        self.broker = Broker_Facade()
        self.queue_consumer = Queue_Adapter()
        # TODO: load number 7 from dotenv(consumer.conf)
        self.lstm = LSTM_Strategy(120)

        self.broker.init_historic_api()
        self.broker.init_trading_api()
        self.queue_consumer.init_consumer()

    def consuming_handler(self, message):
        ticker = message['ticker']
        prices = self.broker.get_data_from_stock(ticker).values.reshape(-1, 1)
        print(f"TICKER - {ticker}")
        prices = self.lstm.predict(prices)
        # TODO: Calculate quantity 
        day_max_price = self.lstm.get_max_prediction(prices)
        self.broker.buy_stock(ticker, 1, day_max_price)
                
    def start_consumer(self):
        self.queue_consumer.start_consuming(self.consuming_handler)

if __name__ == "__main__":
    consumer = Consumer()

    consumer.start_consumer()
