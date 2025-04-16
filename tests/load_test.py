import asyncio
import httpx
import time
import uuid

BASE_URL = "http://localhost:8000/api/v1"
NUM_REQUESTS = 100

client = httpx.AsyncClient()

transaction_ids = []


async def post_transaction():
    transaction_id = str(uuid.uuid4())
    payload = {
        "user_id": "loadtest",
        "transaction_id": transaction_id,
        "amount": 42.0,
        "currency": "USD",
        "category": "test",
        "type": "expense",
        "date": "2025-03-27T00:00:00Z",
        "notes": "Performance test"
    }
    start = time.perf_counter()
    response = await client.post(f"{BASE_URL}/transaction/", json=payload)
    end = time.perf_counter()
    transaction_ids.append(transaction_id)
    return end - start


async def get_transaction(transaction_id):
    start = time.perf_counter()
    response = await client.get(f"{BASE_URL}/transaction/loadtest/{transaction_id}")
    end = time.perf_counter()
    return end - start


async def delete_transaction(transaction_id):
    start = time.perf_counter()
    response = await client.delete(f"{BASE_URL}/transaction/loadtest/{transaction_id}")
    end = time.perf_counter()
    return end - start


async def main():

    print(f"Starting {NUM_REQUESTS} concurrent writes...")
    write_times = await asyncio.gather(*[post_transaction() for _ in range(NUM_REQUESTS)])
    avg_write = sum(write_times) / len(write_times)
    print(f"✅ Avg write time: {avg_write * 1000:.2f} ms")


    print(f"Starting {NUM_REQUESTS} concurrent reads...")
    read_times = await asyncio.gather(*[get_transaction(txn_id) for txn_id in transaction_ids])
    avg_read = sum(read_times) / len(read_times)
    print(f"✅ Avg read time: {avg_read * 1000:.2f} ms")


    print(f"Starting {NUM_REQUESTS} concurrent deletes...")
    delete_times = await asyncio.gather(*[delete_transaction(txn_id) for txn_id in transaction_ids])
    avg_delete = sum(delete_times) / len(delete_times)
    print(f"✅ Avg delete time: {avg_delete * 1000:.2f} ms")

    await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
