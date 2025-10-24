from libs.llm.llm_interface import LLM_Interface
from libs.llm.openai.openai_utils import OpenAI_Client, OpenAI_Rate_Limit

class LLM_Facade(LLM_Interface):
    class Model_Rate_Limit(Exception):
        def __init__(self, msg):
            super().__init__(msg)

    def __init__(self):
        self.openai_client = OpenAI_Client()

    def failover_model(self):
        self.openai_client.failover_openai_model()
        
    def send_prompt(self, prompt):
        try:
            return self.openai_client.prompt_to_chatgpt(prompt)
        except OpenAI_Rate_Limit as e:
            raise LLM_Facade.Model_Rate_Limit(e)
