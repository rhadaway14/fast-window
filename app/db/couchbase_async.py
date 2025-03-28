from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from acouchbase.cluster import Cluster
from app.core.config import settings

cluster = None
collection = None


async def init_couchbase():
    global cluster, collection
    if cluster is None or collection is None:
        cluster = await Cluster.connect(
            settings.COUCHBASE_HOST,
            ClusterOptions(PasswordAuthenticator(
                settings.COUCHBASE_USER,
                settings.COUCHBASE_PASSWORD
            ))
        )
        bucket = cluster.bucket(settings.COUCHBASE_BUCKET)
        await bucket.on_connect()
        scope = bucket.scope(settings.COUCHBASE_SCOPE)
        collection = scope.collection(settings.COUCHBASE_COLLECTION)


async def get_async_collection():
    if collection is None:
        await init_couchbase()
    return collection
