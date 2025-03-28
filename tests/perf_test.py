import asyncio
import httpx
import time

BASE_URL = "http://localhost:8000/api/v1"

test_payload = {
    "user_id": "perf001",
    "transaction_id": "txn123",
    "amount": 100.00,
    "currency": "USD",
    "category": "Performance",
    "type": "expense",
    "date": "2025-03-26T14:30:00Z",
    "notes": "Performance test"
}


async def measure_post_request():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        response = await client.post(f"{BASE_URL}/transaction/", json=test_payload)
        end = time.perf_counter()
        duration_ms = (end - start) * 1000

        print(f"POST /transaction/ took {duration_ms:.2f}ms — Status: {response.status_code}")
        print("Response:", response.json())


async def measure_get_request():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        response = await client.get(f"{BASE_URL}/transaction/{test_payload['user_id']}/{test_payload['transaction_id']}")
        end = time.perf_counter()
        duration_ms = (end - start) * 1000

        print(f"GET /transaction/... took {duration_ms:.2f}ms — Status: {response.status_code}")
        print("Response:", response.json())


async def measure_delete_request():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        response = await client.delete(f"{BASE_URL}/transaction/{test_payload['user_id']}/{test_payload['transaction_id']}")
        end = time.perf_counter()
        duration_ms = (end - start) * 1000

        print(f"DELETE /transaction/... took {duration_ms:.2f}ms — Status: {response.status_code}")
        print("Response:", response.json())


async def main():
    await measure_post_request()
    await measure_get_request()
    await measure_delete_request()

if __name__ == "__main__":
    asyncio.run(main())
