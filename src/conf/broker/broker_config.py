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
    stop_loss_percentage: int = Field(gt=0, description="Must be > 0")
    base_investment: int = Field(gt=0, description="Must be > 0")
    historic_lookback_days: int = Field(gt=0, description="Must be > 0")

    @classmethod
    def load(cls) -> "BrokerConfig":
        loader = ConfigLoader()
        data = loader.get_section("BROKER")

        data["blacklist"] = [x.upper() for x in data["blacklist"]]
        data["api_endpoint"] = str(data["api_endpoint"])

        return cls(**data)
