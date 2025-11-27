from openai import OpenAI, RateLimitError, BadRequestError, APIError
from conf.llm.llm_config import LLMConfig

from libs.log_manager.logger_factory import LoggerFactory

from time import sleep, time
import os
import threading
import shelve

ONE_DAY = 86400
ONE_HOUR = 3600
ONE_MINUTE = 60

class OpenAI_Client:
    # TODO: Max length of 8000 characters (input)
    class OpenAI_Rate_Limit(Exception):
        def __init__(self, model_name, retry_after = None):
            msg = f"Model {model_name} is rate-limited"

            if retry_after is not None:
                msg += f", retry after {retry_after} seconds"

            super().__init__(msg)

    def __init__(self, service_type_who):
        self.log = LoggerFactory(service_type_who)
        self.log.init_logger(self.log.openai)

        self.configuration = LLMConfig.load()
        self.a_model_ready = True
        self.openai_models = self.configuration.openai_models
        self.openai_model_iterator = iter(self.openai_models)
        self.current_openai_model = next(self.openai_model_iterator)
        # Variable AINVEST_PERSISTENT_DIR exported inside Docker container
        self.failover_status_db = os.path.join(os.getenv("AINVEST_PERSISTENT_DIR", ""), "failover_state")
        self.openai_client = OpenAI(
                base_url = self.configuration.base_url,
                api_key = self.configuration.api_key
                )

    def _print_remmaining_reuse_model_time(self, model, elapsed):
        remaining = max(ONE_DAY - elapsed, 0)
        hours = int(remaining // ONE_HOUR)
        minutes = int((remaining % ONE_HOUR) // ONE_MINUTE)
        seconds = int(remaining % ONE_MINUTE)
        remaining_time = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

        self.log.debug(f"Remmaining time to reuse the model {model}: {remaining_time}")

    def _is_model_cold(self, model):
        model_is_cooled = False
        model_not_cold = True

        with shelve.open(self.failover_status_db) as cooldowns:
            model_not_cold = model in cooldowns
            while model in cooldowns and not model_is_cooled:
                elapsed = time() - cooldowns[model] 
                self._print_remmaining_reuse_model_time(model, elapsed)
                model_is_cooled = elapsed >= ONE_DAY
                sleep(ONE_HOUR)

        if model_is_cooled:
            self.log.debug(f"Model {model} is active again. To be re-activated")
        if model_not_cold:
            self.log.debug(f"Model {model} is already active")

        return model_is_cooled or model_not_cold

    def _coldown_request_model(self, model):
        if not self._is_model_cold(model):
            model_priority = self.openai_models.index(model)
            current_model_priority = self.openai_models.index(self.current_openai_model)

            if model_priority > current_model_priority:
                self.current_openai_model = model
                message = f"Model {self.current_openai_model} active back again"
            else:
                message = f"Model {model} ready to work again. Current active model is {self.current_openai_model}"
            self.log.info(message)

            self.a_model_ready = True

            with shelve.open(self.failover_status_db) as cooldowns:
                del cooldowns[model]
                self.log.debug(f"Removed {model} from cooldown DB stored in {self.failover_status_db}")

    def failover_openai_model(self):
        try:
            with shelve.open(self.failover_status_db) as failovers:
                if not self.current_openai_model in failovers:
                    failovers[self.current_openai_model] = time()

            threading.Thread(
                    target = self._coldown_request_model,
                    args = (self.current_openai_model,),
                    daemon = True
                    ).start()
            self.current_openai_model = next(self.openai_model_iterator)
            self.log.info(f"Switching to model {self.current_openai_model}")
        except StopIteration:
            self.log.warning("No more available models to use")
            self.a_model_ready = False
            while not self.a_model_ready:
                sleep(5) # wait 5 seconds

    def prompt_to_chatgpt(self, prompt):
        try:
            self.log.debug(f"Using {self.current_openai_model} openAI model")
            response = self.openai_client.chat.completions.create(
                    messages = [{"role": "user", "content": prompt}],
                    temperature = self.configuration.openai_model_temperature,
                    top_p = self.configuration.openai_model_top_p,
                    model = self.current_openai_model
                    )

            return response.choices[0].message.content.strip()
        except BadRequestError as e:
            err_msg = str(e)
            if 'content_filter' in err_msg:
                self.log.warning("OpenAI content moderation filetered the response. Prompt ignored")
            else:
                self.log.error(f"OpenAI BadRequestError: {err_msg}")
            return None
        except RateLimitError as e:
            raise OpenAI_Client.OpenAI_Rate_Limit(self.current_openai_model)
        except APIError as e:
            self.log.error(f"OpenAI API error: {e}")
            return None

