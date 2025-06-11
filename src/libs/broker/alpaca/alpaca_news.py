from alpaca.data.live import NewsStream
from chatgpt import ChatGPT

import asyncio

class Alpaca_News:
    def __init__(self, api_key, api_secret):
       self.news_stream = NewsStream(api_key, api_secret)

    async def handle_news(news):
        # TODO: create DEEPSEEK and KAFKA classes
       llvm = LLVM(news.headline, news.summary)

    def start(self):
        # TODO: if * does not work create a config file with the stocks and iterate
        # TODO: do multithreaded
       self.news_stream.subscribe(self.handle_news, "*")

