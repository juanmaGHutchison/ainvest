from libs.queue.queue_interface import Queue_Interface
from kafka import KafkaProducer
from kafka import KafkaConsumer

from dotenv import load_dotenv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import redis
import hashlib
import json
import os

class Queue_Adapter(Queue_Interface):
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/kafka.env"
        load_dotenv(dotenv_path.resolve())
        self.KAFKA_SERVER = f"{os.getenv('KAFKA_DOCKER_NAME')}:{os.getenv('KAFKA_PORT')}"
        self.TOPIC = os.getenv("MAIN_TOPIC")

        self.redis_cache = redis.Redis(
                host = os.getenv("REDIS_HOST"),
                port = int(os.getenv("REDIS_PORT")),
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
        message_id = hashlib.sha256(message_raw.encode("utf-8")).hexdigest()

        if not self.redis_cache.get(message_id):
            try:
                self.consumer.commit()
                self.redis_cache.setex(message_id, 86400, "1")
                handler(json.loads(message_raw, strict=False))
            except Exception as e:
                print(f"[ERROR] Processing failed: {e}")

    def start_consuming(self, handler_function):
        self.consumer.subscribe([self.TOPIC])

        for message in self.consumer:
            self.executor.submit(self._handle_message, message, handler_function) 

    def send(self, data):
        self.producer.send(self.TOPIC, data)
        self.producer.flush()

