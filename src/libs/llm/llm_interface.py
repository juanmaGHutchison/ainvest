from abc import ABC, abstractmethod

class LLM_Interface(ABC):
    class ModelRateLimit(Exception):
        pass

    @abstractmethod
    def send_prompt(self, prompt):
        pass

    @abstractmethod
    def failover_model(self):
        pass

