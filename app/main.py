from fastapi import FastAPI
from app.api.v1.routes import router as v1_router
from app.db.couchbase_async import init_couchbase
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="FastAPI with Couchbase", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await init_couchbase()

Instrumentator().instrument(app).expose(app)

app.include_router(v1_router, prefix="/api/v1")
