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

        if (not is_positive_news):
            print(f"Omit {news.symbols} because of Negative news")
        if (not is_not_blacklist):
            print(f"Omit {news.symbols} because it is Blacklisted")
        if (not is_not_opened):
            print(f"Omit {news.symbols} because Symbol has already an open operation")

        return is_positive_news and is_not_blacklist and is_not_opened

    def process_news(self, news):
        if self._pre_filter(news):
            try:
                llm_response = self.llm.send_prompt(
                        self.prompt.prompt_to_json_input(news)
                        )
                print({llm_response})

                self.queue_producer.send(llm_response)
            except LLM_Facade.Model_Rate_Limit as e:
                print(f"[ERROR] {e}")
                self.llm.failover_model()

    def start_producing(self):
        self.broker.fetch_news('*', self.process_news)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()
