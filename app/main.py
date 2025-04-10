from fastapi import FastAPI
from app.api.v1.routes import router as v1_router
from prometheus_fastapi_instrumentator import Instrumentator
from app.db.couchbase_async import get_async_collection

app = FastAPI(title="FastAPI with Couchbase", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await get_async_collection()

Instrumentator().instrument(app).expose(app)

app.include_router(v1_router, prefix="/api/v1")
