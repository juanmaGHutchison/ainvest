from abc import ABC, abstractmethod

class Strategy_Interface(ABC):

    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def get_max_prediction(self, data):
        pass
