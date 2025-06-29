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
        self.lstm = LSTM_Strategy(60)

        self.broker.init_historic_api()
        self.queue_consumer.init_consumer()

    def consuming_handler(self, message):
        print(f"Received: {message.value.decode('utf-8')}")
        message_json = json.loads(message.value.decode('utf-8'))
        ticker = message_json['ticker']

        prices = self.broker.get_data_from_stock(ticker).values.reshape(-1, 1)

        self.lstm.predict(prices)
                
    def start_consumer(self):
        self.queue_consumer.start_consuming(self.consuming_handler)

if __name__ == "__main__":
    consumer = Consumer()

    consumer.start_consumer()
