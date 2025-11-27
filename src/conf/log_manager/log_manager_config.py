#!/usr/bin/env python3
from pydantic import BaseModel, Field, field_validator
from conf.loader import ConfigLoader

class LogManagerConfig(BaseModel):
    config_file: str
    producer: str
    consumer: str
    broker: str
    llm: str
    openai: str
    queue: str
    maths_lstm: str
    prompt_manager: str

    @classmethod
    def load(cls) -> "LogManagerConfig":
        loader = ConfigLoader()
        data = loader.get_section("LOGM")

        return cls(**data)
