from abc import ABC, abstractmethod

class Broker_News_Interface(ABC):

    @abstractmethod
    def fetch_news(stock, what_to_do_func):
        pass
