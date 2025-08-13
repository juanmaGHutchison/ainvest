#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.llvm.llvm_facade import LLVM_Facade
from libs.prompt_manager.prompt_manager import Prompt_Manager

from dotenv import load_dotenv
from pathlib import Path
import os

# Only for dummy data. When unnecessary, delete
import random

class Producer:
    def __init__(self):
        load_dotenv("config/producer.env")
        
        self.broker = Broker_Facade()
        self.queue_producer = Queue_Adapter()
        self.llvm = LLVM_Facade()

        self.queue_producer.init_producer()
        self.broker.init_news_api()
        
    def process_news(self, news):
        prompt = Prompt_Manager()
        self.llvm.send_prompt(prompt.prompt_to_json_input(news))
        print("----------------------")
        print(news)
        print("----------------------")

    def start_producing(self):
        # TODO: what can i do with stocks. Test * and look for other solutions
        # TODO: uncomment to retrieve real data and process it
        self.broker.fetch_news('*', self.process_news)
        # TODO: assemble the JSON message
        # rand_num = random.randint(0, 1000)
        # dummy_good_message = {"ticker": "AAPL", "headline": f"NEW {rand_num}  Good news", "summary": "Summary of good news", "goal": 80}
        # dummy_bad_message = {"ticker": "AAPL", "headline": "NEW Bad news", "summary": "Summary of bad news", "goal": 10}
        
        # self.queue_producer.send(dummy_good_message)
        # self.queue_producer.send(dummy_bad_message)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()

