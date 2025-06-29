from libs.broker.broker_interface import Broker_Interface

from libs.broker.alpaca.alpaca_news import Alpaca_News
from libs.broker.yahoo_finance.yahoo_finance_historic_data import Yahoo_Historic_Data
from libs.broker.alpaca.alpaca_trading import Alpaca_Trading

class Broker_Facade(Broker_Interface):
    def __init__(self):
        self.broker_news: Alpaca_News
        self.broker_historic: Yahoo_Historic_Data
        self.broker_trading: Alpaca_Trading

    def init_news_api(self):
        self.broker_news = Alpaca_News()

    def init_historic_api(self):
        self.broker_historic = Yahoo_Historic_Data()

    def init_trading_api(self):
        self.broker_trading = Alpaca_Trading()

    def fetch_news(self, stock, handler_function):
        self.broker.subscribe_news(handler_function, stock)
        self.broker.run()

    def get_data_from_stock(self, stock):
        # TODO: config file
        n_days_ago = 90
        return self.broker_historic.fetch_historic_prices_from(n_days_ago, stock)

    def buy_stock(self, symbol, notional, limit_price):
       self.broker_trading.buy_stock(symbol, notional, limit_price) 
