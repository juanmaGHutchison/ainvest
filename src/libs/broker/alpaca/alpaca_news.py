from libs.broker.alpaca.alpaca_session import Alpaca_Session
import asyncio

class Alpaca_News(Alpaca_Session):
    def __init__(self):
        super().__init__()
        self.init_alpaca_stream_session()

    def fetch_news(self, stock, process_func):
        self.broker.subscribe_news(process_func, stock)
        self.broker.run()

