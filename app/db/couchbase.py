from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from app.core.config import settings


def get_cluster():
    auth = PasswordAuthenticator(settings.COUCHBASE_USER, settings.COUCHBASE_PASSWORD)
    cluster = Cluster(settings.COUCHBASE_HOST, ClusterOptions(auth))
    return cluster


def get_collection():
    cluster = get_cluster()
    bucket = cluster.bucket(settings.COUCHBASE_BUCKET)
    scope = bucket.scope(settings.COUCHBASE_SCOPE)
    return scope.collection(settings.COUCHBASE_COLLECTION)
