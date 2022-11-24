import io
import json
import logging
from anv.api import ipfs

log = logging.getLogger("anv")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def test_ipfs_download():
    proxy = ipfs.IPFSProxy()
    ipfs_url = "ipfs://Qmd4ZCowwMdttP6W8nVWdxVnDYw1kcVe86aG9QuN9fooKJ/v2.info8749.json"
    ipfs_url = "ipfs://QmdD6oF51J3aWjqsCYQKyuBtYhg69PdK7LGLiHBMqrR8B6/v2.info9443.json"
    result = proxy.get_json(ipfs_url)
    assert result

    with io.BytesIO() as buffer:
        proxy.get_ipfs_binary(ipfs_url, buffer)
        buffer.seek(0)

        result = json.loads(buffer.read())
        assert result


def test_get_binary_ipfs_http_url():
    ipfs_http_url = "https://apricot-payable-centipede-980.mypinata.cloud/ipfs/QmQSf1NZhAASSyYET19FqHbKw3P6AGZKGScSNVREw7PDjt/637.jpg"
    proxy = ipfs.IPFSProxy()
    with io.BytesIO() as buffer:
        proxy.get_binary_from_http_url(ipfs_http_url, buffer)
        buffer.seek(0)

        with open("637.jpg", "wb") as f:
            f.write(buffer.read())
