from alpaca_trade_api import Stream

import asyncio

# TODO: Use this class in the adapter
class Alpaca_News:
    def __init__(self, api_key, api_secret):
        self.broker = Stream(api_key, api_secret)

    def fetch_news(self, stock, process_func):
        self.broker.subscribe_news(process_func, stock)
        self.broker.run()

