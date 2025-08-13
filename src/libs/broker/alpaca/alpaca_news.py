from libs.broker.alpaca.alpaca_session import Alpaca_Session
import asyncio
import inspect

class Alpaca_News(Alpaca_Session):
    def __init__(self):
        super().__init__()
        self.init_alpaca_stream_session()

    def fetch_news(self, stocks, process_func):
        async def handler(news):
            if inspect.iscoroutinefunction(process_func):
                await process_func(news)
            else:
                process_func(news)

        if isinstance(stocks, str):
            stocks = [stocks]

        self.broker.subscribe_news(handler, *stocks)
        self.broker.run()

