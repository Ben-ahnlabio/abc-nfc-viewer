import os
import pymongo


def get_mongo_client() -> pymongo.MongoClient:
    host = os.environ.get("MONGODB_HOST")
    user = os.environ.get("MONGODB_USER")
    password = os.environ.get("MONGODB_PASSWORD")

    """mongodb+srv://ricepotato:<password>@cluster0-gpvm5.gcp.mongodb.net/wetube?retryWrit"""
    connection_string = f"mongodb+srv://{user}:{password}@{host}"
    return pymongo.MongoClient(
        connection_string, ssl=True, tlsAllowInvalidCertificates=True
    )
