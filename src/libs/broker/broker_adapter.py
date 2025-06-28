from libs.broker.broker_interface import Broker_Interface

from libs.broker.alpaca.alpaca_news import Alpaca_News
from libs.broker.alpaca.alpaca_historic_data import Alpaca_Historic_Data
from libs.broker.alpaca.alpaca_trading import Alpaca_Trading

class Broker_Adapter(Broker_Interface):
    def __init__(self):
        self.broker_news: Alpaca_News
        self.broker_historic: Alpaca_Historic_Data
        self.broker_trading: Alpaca_Trading

    def init_news_api(self):
        self.broker_news = Alpaca_News()

    def init_historic_api(self):
        self.broker_historic = Alpaca_Historic_Data()

    def init_trading_api(self):
        self.broker_trading = Alpaca_Trading()

    def fetch_news(self, stock, handler_function):
        self.broker.subscribe_news(handler_function, stock)
        self.broker.run()

    def get_data_from_stock(self, stock):
        # TODO: 120 days
        n_days_ago = 2
        list_of_trades = self.broker_historic.fetch_historic_from(n_days_ago, stock)
        return self.broker_historic.get_prices_from_historic(list_of_trades)

    def buy_stock(self, symbol, notional, limit_price):
       self.broker_trading.buy_stock(symbol, notional, limit_price) 
