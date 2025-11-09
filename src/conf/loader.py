#!/usr/bin/env python3

import os
from pathlib import Path
from threading import Lock
from dotenv import load_dotenv

class ConfigLoader:
    _instance = None
    _lock = Lock()
    _env_file = "config.env"

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init()
            return cls._instance

    def _init(self):
        root_dir = Path(__file__).resolve().parents[1]
        self.env_path = root_dir / self._env_file
        load_dotenv(dotenv_path = self.env_path, override = True)
        self._cache = {}

    def get_section(self, prefix: str, delimiter: str = "__") -> dict:
        prefix = prefix.upper() + delimiter
        if prefix in self._cache:
            return self._cache[prefix]

        section = {
                key[len(prefix):].lower(): value
                for key, value in os.environ.items()
                if key.startswith(prefix)
            }
        self._cache[prefix] = section
        return section

    def reload(self):
        self._cache.clear()
        load_dotenv(dotenv_path = self.env_path, override = True)

