from abc import ABC, abstractmethod

class Strategy_Interface(ABC):

    @abstractmethod
    def predict(self, data):
        pass

