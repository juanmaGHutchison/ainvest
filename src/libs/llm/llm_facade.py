from libs.llm.llm_interface import LLM_Interface
from libs.llm.openai.openai_utils import OpenAI_Client

class LLM_Facade(LLM_Interface):
    def __init__(self):
        self.openai_client = OpenAI_Client()

    def send_prompt(self, prompt):
        return self.openai_client.prompt_to_chatgpt(prompt)
