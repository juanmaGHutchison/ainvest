from dotenv import load_dotenv
from pathlib import Path
from transformers import pipeline
import os

class Prompt_Manager:
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/prompt.env"
        load_dotenv(dotenv_path.resolve())

        self.prompt_tpl = os.getenv("P_PROMPT_TPL")
        self.out_json_format = os.getenv("P_OUT_JSON_FORMAT")

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

