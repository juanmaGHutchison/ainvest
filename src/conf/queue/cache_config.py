#!/usr/bin/env python3
from pydantic import BaseModel, Field
from conf.loader import ConfigLoader

import sys

class CacheConfig(BaseModel):
    host: str
    port: int
    
    @classmethod
    def load(cls) -> "CacheConfig":
        loader = ConfigLoader()
        data = loader.get_section("CACHE")

        return cls(**data)
