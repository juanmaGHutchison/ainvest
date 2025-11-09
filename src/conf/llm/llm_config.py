#!/usr/bin/env python3
from pydantic import BaseModel, Field
from conf.loader import ConfigLoader

class LLMConfig(BaseModel):
    openai_api_key: str
    openai_models: list[str]

    @classmethod
    def load(cls) -> "LLMConfig":
        loader = ConfigLoader()
        data = loader.get_section("LLM")

        data["openai_models"] = [m.strip() for m in data.get("openai_models", "").split(",") if m.strip()]

        return cls(**data)
