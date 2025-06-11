#!/usr/bin/env python3

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca_trade_api import REST, Stream
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# To get old news
# alpaca_rest_client = rest_client.get_news("AAPL", "2021-01-01", "2021-12-31")

alpaca_news_stream = Stream(API_KEY, API_SECRET)

# This will be another program
async def news_data_handler(news):
    print(news)

alpaca_news_stream.subscribe_news(news_data_handler, "AAPL")

alpaca_news_stream.run()

# trading_client = TradingClient(API_KEY, API_SECRET)

# print(trading_client.get_account().account_number)
# print(trading_client.get_account().buying_power)

historic_data_stock = StockHistoricalDataClient(API_KEY, API_SECRET)

today = datetime.today()

historic_data_params = StockTradesRequest(
        symbol_or_symbols = "AAPL",
        start = datetime (2025, 1, 1),
        end = datetime (2025, 1, 2)
        # end = today - timedelta(days=today.weekday())
)

trades = historic_data_stock.get_stock_trades(historic_data_params)
trade_list = trades["AAPL"]

for i in range(len(trade_list)):
    print(trades["AAPL"][i].price)
# json_trades = json.loads(trades)
#
# print(json_trades)
# print (f"PRICE: {json_trades['price']}")
# print(trades)

