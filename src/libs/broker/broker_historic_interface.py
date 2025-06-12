from abc import ABC, abstractmethod


class Broker_Historic_Interface(ABC):

    @abstractmethod
    def get_data_from_stock(stock):
        pass


