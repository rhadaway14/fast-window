from fastapi import APIRouter, HTTPException
from app.models.transaction import Transaction
from app.db.couchbase_async import get_async_collection

router = APIRouter()


@router.get("/healthz")
async def healthz():
    return {"status": "ok"}


@router.delete("/transaction/{user_id}/{transaction_id}")
async def delete_transaction(user_id: str, transaction_id: str):
    key = f"user::{user_id}::trans::{transaction_id}"
    collection = await get_async_collection()
    try:
        await collection.remove(key)
        return {"status": "deleted", "key": key}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Document not found: {key}")


@router.get("/transaction/perftest/{user_id}/{transaction_id}")
async def perf_test_transaction(user_id: str, transaction_id: str):
    collection = await get_async_collection()

    try:
        key1 = f"user::{user_id}::trans::{transaction_id}"
        doc1 = await collection.get(key1)
        data1 = doc1.content_as[dict]

        key2 = data1.get("next_key") or key1
        doc2 = await collection.get(key2)
        data2 = doc2.content_as[dict]

        key3 = data2.get("next_key") or key2
        doc3 = await collection.get(key3)
        data3 = doc3.content_as[dict]

        key4 = data3.get("next_key") or key3
        doc4 = await collection.get(key4)
        data4 = doc4.content_as[dict]

        final_key = f"user::{user_id}::final::{transaction_id}"
        await collection.upsert(final_key, {"summary": data4})

        return {"status": "ok", "written_key": final_key}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transaction/")
async def create_transaction(tx: Transaction):
    key = f"user::{tx.user_id}::trans::{tx.transaction_id}"
    collection = await get_async_collection()
    try:
        await collection.upsert(key, tx.dict())
        return {"status": "success", "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

