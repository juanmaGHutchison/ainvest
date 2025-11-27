import logging.config
import yaml
import os
from pathlib import Path

class LoggerConfig:
    # Flag to configure the LoggerConfig YAML only once
    _configured = False

    def __init__(self, config_path: str, service_type: str):
        self.config_path = Path(config_path)

        # Variable AINVEST_PERSISTENT_DIR exported inside Docker container
        persistence_dir = os.getenv("AINVEST_PERSISTENT_DIR", "")
        self.log_root = service_type
        logging_dir = Path(persistence_dir) / self.log_root
        logging_dir.mkdir(parents = True, exist_ok = True)

    def configure(self):
        if LoggerConfig._configured:
            return

        if not self.config_path.exists():
            raise FileNotFoundError(f"Logger config not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            text = f.read()
        
        text = text.format(log_root = self.log_root)
        config = yaml.safe_load(text)

        logging.config.dictConfig(config)
        LoggerConfig._configured = True
