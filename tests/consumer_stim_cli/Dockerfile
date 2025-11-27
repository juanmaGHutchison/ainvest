FROM python:3.10-slim

WORKDIR /app

COPY consumer_stim.py /app/python_kafka_test_producer.py

RUN pip install --no-cache-dir confluent-kafka

ENTRYPOINT ["python", "/app/python_kafka_test_producer.py"]

