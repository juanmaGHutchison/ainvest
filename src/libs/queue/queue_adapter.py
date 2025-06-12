from libs.queue.queue_interface import Queue_Interface
from kafka import KafkaProducer
from kafka import KafkaConsumer

from dotenv import load_dotenv
from pathlib import Path
import json
import os

class Queue_Adapter(Queue_Interface):
    def __init__(self):
        dotenv_path = Path(__file__).parent / "conf/kafka.env"
        load_dotenv(dotenv_path.resolve())
        self.KAFKA_SERVER = f"{os.getenv('KAFKA_DOCKER_NAME')}:{os.getenv('KAFKA_PORT')}"
        self.TOPIC = os.getenv("MAIN_TOPIC")

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
                enable_auto_commit = True
                )

    def start_consuming(self, what_to_do_func):
        self.consumer.subscribe([self.TOPIC])

        for message in self.consumer:
            what_to_do_func(message)

    def send(self, data):
        self.producer.send(self.TOPIC, data)
        self.producer.flush()

