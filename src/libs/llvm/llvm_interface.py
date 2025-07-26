from abc import ABC, abstractmethod

class LLVM_Interface(ABC):

    @abstractmethod
    def send_prompt(self, prompt):
        pass
