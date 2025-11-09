#!/usr/bin/env python3
from pydantic import BaseModel, Field
from conf.loader import ConfigLoader

class PromptManagerConfig(BaseModel):
    input_tpl: str
    output_tpl: str

    @classmethod
    def load(cls) -> "PromptManagerConfig":
        loader = ConfigLoader()
        data = loader.get_section("PROMPT")

        return cls(**data)
