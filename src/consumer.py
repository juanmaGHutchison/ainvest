#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.maths.lstm_strategy import LSTM_Strategy

import numpy as np

class Consumer:
    def __init__(self):
        self.broker = Broker_Facade()
        self.queue_consumer = Queue_Adapter()
        # TODO: load number () from dotenv(consumer.conf)
        self.lstm = LSTM_Strategy(60)

        self.broker.init_historic_api()
        self.broker.init_trading_api()
        self.queue_consumer.init_consumer()

    def consuming_handler(self, message):
        ticker = message['ticker']
        prices = self.broker.get_data_from_stock(ticker).values.reshape(-1, 1)
        latest_price = float(prices[-1].item())
        # TODO: put 0.6 in config file. I.E. Close OP if 40% loss
        stop_loss_price = latest_price * 0.9
        print(f"Current {ticker} share price: {latest_price}")
        print(f"Stop loss price: {stop_loss_price}")
        prices = self.lstm.predict(prices)
        mean_prediction_price = float(np.mean(prices))
        target_price = max (mean_prediction_price, latest_price * 1.02)
        print(f"Target price: {target_price}")
        self.broker.buy_stock(ticker, latest_price, target_price, stop_loss_price)
        print("--------------------------")
                
    def start_consumer(self):
        self.queue_consumer.start_consuming(self.consuming_handler)

if __name__ == "__main__":
    consumer = Consumer()

    consumer.start_consumer()
