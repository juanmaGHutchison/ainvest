#!/usr/bin/env python3

from libs.broker.broker_news_adapter import Broker_News_Adapter

from kafka import KafkaProducer

from dotenv import load_dotenv
from pathlib import Path
import os
import json

async def process_news(news):
    print("buscando newses")
    print(news)

if __name__ == "__main__":
    load_dotenv("config/alpaca.env")
    load_dotenv("config/kafka.env")
    load_dotenv("config/producer.env")

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    # broker_news = Broker_News_Adapter(API_KEY, API_SECRET)
    # broker_news.fetch_news("AAPL", process_news)

    KAFKA_SERVER = f"{os.getenv('KAFKA_DOCKER_NAME')}:{os.getenv('KAFKA_PORT')}"
    TOPIC = os.getenv("MAIN_TOPIC")

    producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    dummy_good_message = {"ticker": "AAPL", "headline": "Good news", "summary": "Summary of good news", "goal": 80}
    dummy_bad_message = {"ticker": "AAPL", "headline": "Bad news", "summary": "Summary of bad news", "goal": 10}
    producer.send(TOPIC, dummy_good_message)
    producer.send(TOPIC, dummy_bad_message)

    producer.flush()

