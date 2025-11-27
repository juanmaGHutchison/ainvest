from conf.prompt_manager.prompt_manager_config import PromptManagerConfig
from libs.log_manager.logger_factory import LoggerFactory

from transformers import pipeline

class Prompt_Manager:
    def __init__(self, logger_service_who):
        self.log = LoggerFactory(logger_service_who)
        self.log.init_logger(self.log.prompt_manager)

        self.configuration = PromptManagerConfig.load()
        self.prompt_tpl = self.configuration.input_tpl
        self.out_json_format = self.configuration.output_tpl

        self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model = "distilbert-base-uncased-finetuned-sst-2-english"
                )

    def prompt_to_json_input(self, in_json):
        filter_json = self.prompt_tpl % (in_json, self.out_json_format)
        filter_json = filter_json.encode("utf-8", "replace").decode("unicode_escape")
        filter_json = filter_json.replace("\xa0", " ")

        return filter_json

    def is_positive_news(self, news):
        result = self.sentiment_pipeline(news.headline)[0]

        return result['label'] == 'POSITIVE' and result['score'] > 0.8

