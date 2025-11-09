#!/usr/bin/env python3
from pydantic import BaseModel, Field
from conf.loader import ConfigLoader

import sys

class QueueConfig(BaseModel):
    docker_name: str
    port: int
    main_topic: str
    
    @classmethod
    def load(cls) -> "QueueConfig":
        loader = ConfigLoader()
        data = loader.get_section("QUEUE")

        return cls(**data)
