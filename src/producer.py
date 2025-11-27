#!/usr/bin/env python3

from libs.broker.broker_facade import Broker_Facade
from libs.queue.queue_adapter import Queue_Adapter
from libs.llm.llm_facade import LLM_Facade
from libs.prompt_manager.prompt_manager import Prompt_Manager
from libs.log_manager.logger_factory import LoggerFactory

class Producer:
    def __init__(self):
        logger_service_type = self.__class__.__name__
        self.log = LoggerFactory(logger_service_type)
        self.log.init_logger(self.log.producer)

        self.broker = Broker_Facade(logger_service_type)
        self.queue_producer = Queue_Adapter(logger_service_type)
        self.llm = LLM_Facade(logger_service_type)

        self.queue_producer.init_producer()
        self.broker.init_news_api()
        self.broker.init_trading_api()
        self.prompt = Prompt_Manager(logger_service_type)

    def _pre_filter(self, news):
        ticker = news.symbols
        is_positive_news = self.prompt.is_positive_news(news)
        is_not_blacklist = not self.broker.is_blacklisted(ticker)
        is_not_opened = not self.broker.is_already_open(ticker)
        is_under_threshold_invest = self.broker.is_under_threshold_invest(ticker)

        if (not is_positive_news):
            message = "Negative news. Skipping"
            self.log.debug(message, ticker)
        if (not is_not_blacklist):
            message = "Blacklisted ticker. Skipping"
            self.log.debug(message, ticker)
        if (not is_not_opened):
            message = "Ticker has already an open operation. Skipping" 
            self.log.debug(message, ticker)
        if (is_under_threshold_invest):
            message = "Price of a share is more expensive than configured threshold in app. Skipping"
            self.log.debug(message, ticker)

        return is_positive_news and is_not_blacklist and is_not_opened and not is_under_threshold_invest

    def process_news(self, news):
        ticker = news.symbols
        if self._pre_filter(news):
            llm_response = self.llm.send_prompt(
                    self.prompt.prompt_to_json_input(news)
                    )
            self.log.info({llm_response}, ticker)

            self.queue_producer.send(llm_response)
        else:
            message = "Ticker did not pass pre-filters. Skipping"
            self.log.info(message, ticker) 

    def start_producing(self):
        self.broker.fetch_news('*', self.process_news)

if __name__ == "__main__":
    producer = Producer()
    producer.start_producing()
