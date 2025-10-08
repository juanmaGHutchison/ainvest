#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.llm.llm_facade import LLM_Facade
from libs.prompt_manager.prompt_manager import Prompt_Manager

class Producer:
    def __init__(self):
        self.broker = Broker_Facade()
        self.queue_producer = Queue_Adapter()
        self.llm = LLM_Facade()

        self.queue_producer.init_producer()
        self.broker.init_news_api()
        self.prompt = Prompt_Manager()

    def process_news(self, news):
        if self.prompt.is_positive_news(news) and not self.broker.is_blacklisted(news.symbols):
            llm_response = self.llm.send_prompt(
                    self.prompt.prompt_to_json_input(news)
                    )
            print({llm_response})

            self.queue_producer.send(llm_response)

    def start_producing(self):
        self.broker.fetch_news('*', self.process_news)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()
