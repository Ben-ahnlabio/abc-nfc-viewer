import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "abc-nft-368700-5bb7335d7c2f.json"


def test_storage():
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())
    assert buckets
