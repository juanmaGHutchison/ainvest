#!/usr/bin/env python3
from pydantic import BaseModel, Field
from conf.loader import ConfigLoader

class MathsConfig(BaseModel):
    window_size_days: int = Field(gt=0, description="Must be > 0")

    @classmethod
    def load(cls) -> "LLMConfig":
        loader = ConfigLoader()
        data = loader.get_section("MATHS")

        return cls(**data)
