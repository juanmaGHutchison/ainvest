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
        self.broker.init_trading_api()
        self.prompt = Prompt_Manager()

    def _pre_filter(self, news):
        is_positive_news = self.prompt.is_positive_news(news)
        is_not_blacklist = not self.broker.is_blacklisted(news.symbols)
        is_not_opened = not self.broker.is_already_open(news.symbols)
        is_under_threshold_invest = self.broker.is_under_threshold_invest(news.symbols)

        if (not is_positive_news):
            print(f"[DEBUG] Skipping news for {news.symbols}: Negative news")
        if (not is_not_blacklist):
            print(f"[DEBUG] Skipping news for {news.symbols}: Blacklisted")
        if (not is_not_opened):
            print(f"[DEBUG] Skipping news for {news.symbols}: Symbol has already an open operation")
        if (is_under_threshold_invest):
            print(f"[DEBUG] Skipping news for {news.symbols}: Price of a share is more expensive than configured threshold in app")

        return is_positive_news and is_not_blacklist and is_not_opened and not is_under_threshold_invest

    def process_news(self, news):
        if self._pre_filter(news):
            llm_response = self.llm.send_prompt(
                    self.prompt.prompt_to_json_input(news)
                    )
            print({llm_response})

            self.queue_producer.send(llm_response)
        else:
            print(f"[INFO] Skipping news for {news.symbols}: did not pass pre-filters") 

    def start_producing(self):
        self.broker.fetch_news('*', self.process_news)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()
