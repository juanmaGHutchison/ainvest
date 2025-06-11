from alpaca_trade_api import Stream

from libs.broker.broker_news_interface import Broker_News_Interface

class Broker_News_Adapter(Broker_News_Interface):
    def __init__(self, api_key, api_secret):
        self.broker = Stream(api_key, api_secret)

    def fetch_news(self, stock, process_func):
        self.broker.subscribe_news(process_func, stock)
        self.broker.run()

