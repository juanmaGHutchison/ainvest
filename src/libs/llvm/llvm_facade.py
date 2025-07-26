from libs.llvm.llvm_interface import LLVM_Interface
from libs.llvm.openai.openai_utils import OpenAI_Client

class LLVM_Facade(LLVM_Interface):
    def __init__(self):
        self.openai_client = OpenAI_Client()

    def send_prompt(self, prompt):
        return self.openai_client.prompt_to_chatgpt(prompt)
