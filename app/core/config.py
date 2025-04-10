from dotenv import load_dotenv
import os

# load_dotenv()


class Settings:
    COUCHBASE_HOST = os.getenv("COUCHBASE_HOST")
    COUCHBASE_BUCKET = os.getenv("COUCHBASE_BUCKET")
    COUCHBASE_SCOPE = os.getenv("COUCHBASE_SCOPE")
    COUCHBASE_COLLECTION = os.getenv("COUCHBASE_COLLECTION")
    COUCHBASE_USER = os.getenv("COUCHBASE_USER")
    COUCHBASE_PASSWORD = os.getenv("COUCHBASE_PASSWORD")


settings = Settings()
