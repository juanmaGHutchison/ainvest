#!/usr/bin/env python3

from libs.broker.broker_news_adapter import Broker_News_Adapter

from dotenv import load_dotenv
from pathlib import Path
import os

async def fumada(news):
    print("buscando newses")
    print(news)

if __name__ == "__main__":
    load_dotenv(Path("config/alpaca.env"))

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    broker_news = Broker_News_Adapter(API_KEY, API_SECRET)
    broker_news.fetch_news("AAPL", fumada)
