from fastapi import APIRouter, HTTPException
from app.models.transaction import Transaction
from app.db.couchbase_async import get_async_collection

router = APIRouter()


@router.delete("/transaction/{user_id}/{transaction_id}")
async def delete_transaction(user_id: str, transaction_id: str):
    key = f"user::{user_id}::trans::{transaction_id}"
    collection = await get_async_collection()
    try:
        await collection.remove(key)
        return {"status": "deleted", "key": key}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Document not found: {key}")


@router.get("/transaction/{user_id}/{transaction_id}")
async def read_transaction(user_id: str, transaction_id: str):
    key = f"user::{user_id}::trans::{transaction_id}"
    collection = await get_async_collection()
    try:
        result = await collection.get(key)
        return result.content_as[dict]
    except Exception:
        raise HTTPException(status_code=404, detail="Transaction not found")


@router.post("/transaction/")
async def create_transaction(tx: Transaction):
    key = f"user::{tx.user_id}::trans::{tx.transaction_id}"
    collection = await get_async_collection()
    try:
        await collection.upsert(key, tx.dict())
        return {"status": "success", "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
