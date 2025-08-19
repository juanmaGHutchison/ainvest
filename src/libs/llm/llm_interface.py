from abc import ABC, abstractmethod

class LLM_Interface(ABC):

    @abstractmethod
    def send_prompt(self, prompt):
        pass
