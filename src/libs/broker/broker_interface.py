from abc import ABC, abstractmethod

class Broker_Interface(ABC):

    @abstractmethod
    def init_news_api(self):
        pass

    @abstractmethod
    def init_historic_api(self):
        pass

    @abstractmethod
    def init_trading_api(self):
        pass

    @abstractmethod
    def fetch_news(self, stock, what_to_do_func):
        pass

    @abstractmethod
    def get_data_from_stock(self, stock):
        pass

    @abstractmethod
    def buy_stock(symbol, latest_value, target_price, stop_loss_price):
        pass

    @abstractmethod
    def is_blacklisted(symbol, symbols):
        pass
