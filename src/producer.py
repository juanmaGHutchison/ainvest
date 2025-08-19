#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.llm.llm_facade import LLM_Facade
from libs.prompt_manager.prompt_manager import Prompt_Manager

from dotenv import load_dotenv
from pathlib import Path
import os

class Producer:
    def __init__(self):
        load_dotenv("config/producer.env")
        
        self.broker = Broker_Facade()
        self.queue_producer = Queue_Adapter()
        self.llm = LLM_Facade()

        self.queue_producer.init_producer()
        self.broker.init_news_api()
        
    def process_news(self, news):
        prompt = Prompt_Manager()
        llm_response = self.llm.send_prompt(prompt.prompt_to_json_input(news))
        print(f"SEND: {llm_response}")
        self.queue_producer.send(llm_response)
        

    def start_producing(self):
        self.broker.fetch_news('*', self.process_news)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()

