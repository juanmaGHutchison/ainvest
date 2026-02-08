#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import Literal
from conf.loader import ConfigLoader
from enum import Enum

class Strategies_enum(str, Enum):
    LSTM = "LSTM"
    HLSTM = "HybridLSTM"

class MathsConfig(BaseModel):
    window_size_days: int = Field(gt=0, description="Must be > 0")
    window_size_horizon: int = Field(gt=0, description="Must be > 0")
    strategy_used: Literal[tuple(strat.value for strat in Strategies_enum)]
    training_strategy_dir: str

    @classmethod
    def load(cls) -> "LLMConfig":
        loader = ConfigLoader()
        data = loader.get_section("MATHS")

        return cls(**data)
