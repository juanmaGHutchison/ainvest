#!/usr/bin/env python3
from pydantic import BaseModel, Field, HttpUrl, field_validator
from conf.loader import ConfigLoader

class LLMConfig(BaseModel):
    api_key: str
    base_url: HttpUrl
    openai_models: list[str]
    openai_model_temperature: float = Field(ge=0.0, le=2.0)
    openai_model_top_p: float = Field(ge=0.0, le=1.0)

    @field_validator("base_url", mode="after")
    def conver_base_url_to_str(cls, v):
        return str(v)

    @classmethod
    def load(cls) -> "LLMConfig":
        loader = ConfigLoader()
        data = loader.get_section("LLM")

        data["openai_models"] = [m.strip() for m in data.get("openai_models", "").split(",") if m.strip()]

        return cls(**data)
