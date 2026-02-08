from abc import ABC, abstractmethod
from libs.maths.market_window import MarketWindow

class Predict_Interface(ABC):

    @abstractmethod
    def predict(self, ticker: str, data: MarketWindow):
        pass

    @abstractmethod
    def get_strategy_name(self):
        pass

class Training_Interface(ABC):

    @abstractmethod
    def get_strategy_name(self):
        pass

