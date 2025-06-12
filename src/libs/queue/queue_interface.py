from abc import ABC, abstractmethod

class Queue_Interface(ABC):

    @abstractmethod
    def init_producer(self):
        pass

    @abstractmethod
    def init_consumer(self):
        pass

    @abstractmethod
    def send(self, data):
        pass

    @abstractmethod
    def start_consuming(self, what_to_do_func):
        pass
