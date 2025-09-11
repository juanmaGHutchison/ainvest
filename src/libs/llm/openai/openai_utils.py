from openai import OpenAI

from dotenv import load_dotenv
from pathlib import Path
import os

# TODO: Max length of 8000 characters (input)

class OpenAI_Client:
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/openai.env"
        load_dotenv(dotenv_path.resolve())

        self.openai_client = OpenAI(
                base_url = "https://models.github.ai/inference",
                api_key = os.getenv("OPENAI_API_KEY")
                )

    def prompt_to_chatgpt(self, prompt):
        # TODO: put temperature and top_p in dotenv
        response = self.openai_client.chat.completions.create(
                messages = [{"role": "user", "content": prompt}],
                temperature = 0.7,
                top_p = 1.0,
                model = "gpt-4.1-mini"
                )

        return response.choices[0].message.content.strip()
