#!/bin/bash

docker run --rm \
  --network broker-net \
  -v $(pwd)/messages.txt:/app/messages.txt \
  kafka-test-producer \
  --bootstrap kafka:9092 \
  --topic generic_stock \
  --file /app/messages.txt

