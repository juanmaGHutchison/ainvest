#!/usr/bin/env python3

from libs.broker.broker_adapter import Broker_Adapter
from libs.queue.queue_adapter import Queue_Adapter

from dotenv import load_dotenv
from pathlib import Path
import os

class Producer:
    def __init__(self):
        load_dotenv("config/producer.env")
        
        self.broker = Broker_Adapter()
        self.queue_producer = Queue_Adapter()

        self.queue_producer.init_producer()
        self.broker.init_news_api()
        
    async def process_news(self, news):
        print("buscando newses")
        print(news)

    def start_producing(self):
        # TODO: what can i do with stocks. Test * and look for other solutions
        # TODO: uncomment to retrieve real data and process it
        # self.broker.fetch_news('AAPL', self.process_news)
        # TODO: assemble the JSON message
        dummy_good_message = {"ticker": "AAPL", "headline": "NEW Good news", "summary": "Summary of good news", "goal": 80}
        dummy_bad_message = {"ticker": "AAPL", "headline": "NEW Bad news", "summary": "Summary of bad news", "goal": 10}
        
        self.queue_producer.send(dummy_good_message)
        self.queue_producer.send(dummy_bad_message)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()

