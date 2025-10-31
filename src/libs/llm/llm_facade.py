from libs.llm.llm_interface import LLM_Interface
from libs.llm.openai.openai_utils import OpenAI_Client

class LLM_Facade(LLM_Interface):
    def __init__(self):
        self.openai_client = OpenAI_Client()

    def failover_model(self):
        self.openai_client.failover_openai_model()
        
    def send_prompt(self, prompt):
        try:
            return self.openai_client.prompt_to_chatgpt(prompt)
        except OpenAI_Client.OpenAI_Rate_Limit as e:
            print(f"[ERROR] {e}")
            self.failover_model()

