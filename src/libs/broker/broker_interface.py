from abc import ABC, abstractmethod

class Broker_Interface(ABC):

    @abstractmethod
    def init_historic_api(self):
        pass

    @abstractmethod
    def fetch_news(self, stock, what_to_do_func):
        pass

    @abstractmethod
    def get_data_from_stock(self, stock):
        pass
