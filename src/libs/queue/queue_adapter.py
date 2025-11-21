from libs.queue.queue_interface import Queue_Interface
from conf.queue.queue_config import QueueConfig
from conf.queue.cache_config import CacheConfig

from kafka import KafkaProducer
from kafka import KafkaConsumer

from concurrent.futures import ThreadPoolExecutor

import redis
import hashlib
import json
import os

class Queue_Adapter(Queue_Interface):
    def __init__(self):
        self.kafka_configuration = QueueConfig.load()
        self.redis_configuration = CacheConfig.load()
        self.KAFKA_SERVER = f"{self.kafka_configuration.docker_name}:{self.kafka_configuration.port}"
        self.TOPIC = self.kafka_configuration.main_topic

        self.redis_cache = redis.Redis(
                host = self.redis_configuration.host,
                port = self.redis_configuration.port,
                db = 0
            )

        self.executor: ThreadPoolExecutor

        self.producer: KafkaProducer
        self.consumer: KafkaConsumer

    def init_producer(self):
        self.producer = KafkaProducer(
                bootstrap_servers=self.KAFKA_SERVER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )

    def init_consumer(self):
        self.consumer = KafkaConsumer(
                bootstrap_servers=self.KAFKA_SERVER,
                group_id = 'consumer-1',
                auto_offset_reset = 'earliest',
                enable_auto_commit = False,
                max_poll_interval_ms = 86400000, # 1 day
                session_timeout_ms = 10000,
                value_deserializer=lambda v: json.loads(v.decode("utf-8"))
                )
        self.executor = ThreadPoolExecutor(max_workers = os.cpu_count())
    
    def _handle_message(self, message, handler):
        message_raw = message.value
        message_json = json.loads(message_raw)
        message_id = hashlib.sha256(
                json.dumps(message_raw, sort_keys=True).encode("utf-8")
            ).hexdigest()

        if not self.redis_cache.get(message_id):
            try:
                self.consumer.commit()
                self.redis_cache.setex(message_id, 86400, "1")
                handler(message_json)
            except Exception as e:
                print(f"[ERROR] Processing failed: {e}")
                print("--------------------------")

    def start_consuming(self, handler_function):
        self.consumer.subscribe([self.TOPIC])

        for message in self.consumer:
            self.executor.submit(self._handle_message, message, handler_function) 

    def send(self, data):
        data_to_json = json.loads(data)

        if data_to_json["score"] > self.kafka_configuration.score_threshold:
            self.producer.send(self.TOPIC, data)
            self.producer.flush()

