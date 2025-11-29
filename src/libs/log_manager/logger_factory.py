import logging

from libs.log_manager.logger_config import LoggerConfig
from conf.log_manager.log_manager_config import LogManagerConfig

class LoggerFactory:
    def __init__(self, service_type):
        cfg = LogManagerConfig.load()

        self._producer = cfg.producer
        self._consumer = cfg.consumer
        self._broker = cfg.broker
        self._llm = cfg.llm
        self._openai = cfg.openai
        self._queue = cfg.queue
        self._maths_lstm = cfg.maths_lstm
        self._prompt_manager = cfg.prompt_manager

        self.allowed_classnames = {
            self._producer,
            self._consumer,
            self._broker,
            self._llm,
            self._openai,
            self._queue,
            self._maths_lstm,
            self._prompt_manager,
        }

        self.logger: logging

        self.service_type = service_type
        self.config = LoggerConfig(cfg.config_file, self.service_type)
        self.config.configure()

    def init_logger(self, classname):
        if classname not in self.allowed_classnames:
            raise ValueError(f"Log classname {classname} not allowed")

        self.logger = logging.getLogger(classname)

    def _parse_msg(self, entity, message):
        return f"{self.service_type}|{entity}|{message}"

    def debug(self, message, entity = "Unknown"):
        self.logger.debug(self._parse_msg(entity, message))

    def info(self, message, entity = "Unknown"):
        self.logger.info(self._parse_msg(entity, message))

    def warning(self, message, entity = "Unknown"):
        self.logger.warning(self._parse_msg(entity, message))
        
    def error(self, message, entity = "Unknown"):
        self.logger.error(self._parse_msg(entity, message))

    def critical(self, message, entity = "Unknown"):
        self.logger.critical(self._parse_msg(entity, message))

    @property
    def producer(self):
        return self._producer

    @property
    def consumer(self):
        return self._consumer

    @property
    def broker(self):
        return self._broker

    @property
    def llm(self):
        return self._llm

    @property
    def openai(self):
        return self._openai

    @property
    def queue(self):
        return self._queue

    @property
    def maths_lstm(self):
        return self._maths_lstm

    @property
    def prompt_manager(self):
        return self._prompt_manager
