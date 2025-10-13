from libs.broker.broker_interface import Broker_Interface

from libs.broker.alpaca.alpaca_news import Alpaca_News
from libs.broker.yahoo_finance.yahoo_finance_historic_data import Yahoo_Historic_Data
from libs.broker.alpaca.alpaca_trading import Alpaca_Trading

from math import floor
from dotenv import load_dotenv
from pathlib import Path
import os

class Broker_Facade(Broker_Interface):
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/broker.env"
        load_dotenv(dotenv_path.resolve())
        self.blacklist = os.getenv("BLACKLIST", "")
        self.blacklist = [s.strip() for s in self.blacklist.split(",") if s.strip()]
        self.blacklist = [s.upper() for s in self.blacklist]

        self.broker_news: Alpaca_News
        self.broker_historic: Yahoo_Historic_Data
        self.broker_trading: Alpaca_Trading

        # TODO: put in config file
        # This is the money to spend as base. If operation is very good, more will be spent
        self.base_investment = 5

    def init_news_api(self):
        self.broker_news = Alpaca_News()

    def init_historic_api(self):
        self.broker_historic = Yahoo_Historic_Data()

    def init_trading_api(self):
        self.broker_trading = Alpaca_Trading()

    def fetch_news(self, stock, handler_function):
        self.broker_news.fetch_news(stock, handler_function)

    def get_data_from_stock(self, stock):
        # TODO: config file
        n_days_ago = 90
        return self.broker_historic.fetch_historic_prices_from(n_days_ago, stock)

    def buy_stock(self, symbol, latest_value, target_price, stop_loss_price):
        gap_of_goodness = (target_price - latest_value) / latest_value
        investment = self.base_investment * (1 + gap_of_goodness)
        balance = float(self.broker_trading.get_current_balance())

        qty = max(floor(investment/latest_value), 1) 
        total_cost = qty * latest_value

        has_cash = balance >= total_cost
        worthwhile_operation = qty >= 1

        if has_cash and worthwhile_operation:
            self.broker_trading.buy_sell_stock(symbol, qty, target_price, stop_loss_price)
        else:
            # TODO: Use log files
            if not has_cash:
                print (f"⚠️  Account balance is {balance} and investment requires {total_cost}€. Ignoring operation")
            if not worthwhile_operation:
                print (f"QTY to sell will be less than 1. This operation is worthless")

    def is_blacklisted(self, symbols):
        if isinstance(symbols, str):
            symbols = [symbols]
        elif not symbols:
            symbols = []

        return any(symbol in self.blacklist for symbol in symbols)

