from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from acouchbase.cluster import Cluster
from app.core.config import settings

_cluster = None
_collection = None


async def get_cluster():
    global _cluster
    if _cluster is None:
        _cluster = await Cluster.connect(
            settings.COUCHBASE_HOST,
            ClusterOptions(PasswordAuthenticator(
                settings.COUCHBASE_USER,
                settings.COUCHBASE_PASSWORD
            ))
        )
    return _cluster


async def get_async_collection():
    global _collection
    if _collection is None:
        cluster = await get_cluster()
        bucket = cluster.bucket(settings.COUCHBASE_BUCKET)
        await bucket.on_connect()
        scope = bucket.scope(settings.COUCHBASE_SCOPE)
        _collection = scope.collection(settings.COUCHBASE_COLLECTION)
    return _collection
