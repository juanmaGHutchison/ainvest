#!/usr/bin/env python3
from pydantic import BaseModel, Field, HttpUrl
from conf.loader import ConfigLoader

import sys

class BrokerConfig(BaseModel):
    api_endpoint: HttpUrl
    api_key: str
    api_secret: str
    blacklist: list[str] = Field(default_factory = list)
    max_invest: float = sys.float_info.max

    @classmethod
    def load(cls) -> "BrokerConfig":
        loader = ConfigLoader()
        data = loader.get_section("BROKER")

        data["blacklist"] = [x.upper() for x in data["blacklist"]]

        return cls(**data)
