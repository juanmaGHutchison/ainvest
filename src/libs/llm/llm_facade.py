from libs.llm.llm_interface import LLM_Interface
from libs.llm.openai.openai_utils import OpenAI_Client

from libs.log_manager.logger_factory import LoggerFactory

class LLM_Facade(LLM_Interface):
    def __init__(self, logger_service_who):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.llm)

        self.openai_client = OpenAI_Client(logger_service_who)

    def failover_model(self):
        self.openai_client.failover_openai_model()
        
    def send_prompt(self, prompt):
        try:
            return self.openai_client.prompt_to_chatgpt(prompt)
        except OpenAI_Client.OpenAI_Rate_Limit as e:
            self.log.warning(f"{e}", self.openai_client.get_current_openai_model())
            self.failover_model()
            return self.openai_client.prompt_to_chatgpt(prompt)

