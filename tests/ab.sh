#!/bin/bash

# URL to test
URL="http://localhost:8000/api/v1/transaction/loadtest/txn123"

# Number of requests and concurrency level
REQUESTS=10000
CONCURRENCY=10

echo "Starting Apache Benchmark load loop..."
echo "Target: $URL"
echo "Requests: $REQUESTS | Concurrency: $CONCURRENCY"
echo "Press Ctrl+C to stop."

while true; do
    ab -n $REQUESTS -c $CONCURRENCY "$URL"
    echo "Sleeping for 10 seconds..."
    sleep 10
done
