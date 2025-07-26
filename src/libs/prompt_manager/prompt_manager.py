from dotenv import load_dotenv
from pathlib import Path
import os

class Prompt_Manager:
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/prompt.env"
        load_dotenv(dotenv_path.resolve())

        self.prompt_tpl = os.getenv("P_PROMPT_TPL")
        self.out_json_format = os.getenv("P_OUT_JSON_FORMAT")

    def prompt_to_json_input(self, in_json):
        return self.prompt_tpl % (input_json, self.out_json_format)

    def prompt_to_string(self, out_json):
        # TODO
        print("TODO prompt_to_string - Prompt_Manager")
        return 0
