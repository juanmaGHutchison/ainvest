#!/usr/bin/env python3
import json
import time
from confluent_kafka import Producer
import argparse
import sys


# ------------------------------
# Colors for readable output
# ------------------------------
class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    END = "\033[0m"


# ------------------------------
# Producer configuration
# ------------------------------
def create_producer(bootstrap):
    print(f"{Color.BLUE}[INFO] Connecting to Kafka @ {bootstrap}{Color.END}")

    return Producer({
        "bootstrap.servers": bootstrap,
        "socket.timeout.ms": 5000,
        "message.timeout.ms": 10000,
        "client.id": "python-test-producer"
    })


# ------------------------------
# Delivery callback
# ------------------------------
def delivery_report(err, msg):
    if err is not None:
        print(f"{Color.RED}[ERROR] Delivery failed: {err}{Color.END}")
    else:
        print(
            f"{Color.GREEN}[OK] Message delivered to {msg.topic()} [partition {msg.partition()}]{Color.END}"
        )


# ------------------------------
# Load JSON message from file
# ------------------------------
def load_messages_from_file(path):
    print(f"{Color.BLUE}[INFO] Reading messages from {path}{Color.END}")
    messages = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"{Color.RED}[ERROR] Invalid JSON line: {line}{Color.END}")
                print(e)
                sys.exit(1)

    print(f"{Color.GREEN}[INFO] Loaded {len(messages)} JSON messages{Color.END}")
    return messages


# ------------------------------
# Send a single JSON dict
# ------------------------------
def send_message(producer, topic, data):
    try:
        payload = json.dumps(data)
        producer.produce(topic, payload, callback=delivery_report)
        producer.flush()
    except Exception as e:
        print(f"{Color.RED}[ERROR] Failed to send message: {e}{Color.END}")


# ------------------------------
# Main
# ------------------------------
def main():
    parser = argparse.ArgumentParser(description="Kafka JSON Test Producer")

    parser.add_argument("--bootstrap", default="localhost:9092",
                        help="Kafka bootstrap servers")
    parser.add_argument("--topic", required=True,
                        help="Kafka topic to publish to")

    parser.add_argument("--message", help="Send a single JSON message")
    parser.add_argument("--file", help="Send all JSON lines from file")

    args = parser.parse_args()

    producer = create_producer(args.bootstrap)

    # Option 1 → single JSON message
    if args.message:
        try:
            data = json.loads(args.message)
        except json.JSONDecodeError:
            print(f"{Color.RED}[ERROR] Invalid JSON provided in --message{Color.END}")
            sys.exit(1)

        print(f"{Color.YELLOW}[INFO] Sending single message...{Color.END}")
        send_message(producer, args.topic, data)
        return

    # Option 2 → load multiple JSON messages from file
    if args.file:
        messages = load_messages_from_file(args.file)
        print(f"{Color.YELLOW}[INFO] Sending {len(messages)} messages...{Color.END}")

        for m in messages:
            send_message(producer, args.topic, m)
            time.sleep(0.3)  # slow down to simulate real feed

        return

    print(f"{Color.RED}[ERROR] You must specify --message or --file{Color.END}")


if __name__ == "__main__":
    main()

