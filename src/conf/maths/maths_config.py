#!/usr/bin/env python3
from pydantic import BaseModel, Field
from conf.loader import ConfigLoader

class MathsConfig(BaseModel):
    @classmethod
    def load(cls) -> "LLMConfig":
        loader = ConfigLoader()
        data = loader.get_section("MATHS")

        # TODO

        return cls(**data)
