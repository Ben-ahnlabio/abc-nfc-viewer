import logging
import pathlib
import tempfile
from anv.api import ipfs

log = logging.getLogger("anv")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def test_ipfs_download():
    gateway = ipfs.IPFSGateway()
    ipfs_url = "ipfs://Qmd4ZCowwMdttP6W8nVWdxVnDYw1kcVe86aG9QuN9fooKJ/v2.info8749.json"
    ipfs_url = "ipfs://QmdD6oF51J3aWjqsCYQKyuBtYhg69PdK7LGLiHBMqrR8B6/v2.info9443.json"
    with tempfile.TemporaryDirectory() as dir:
        output_filepath = pathlib.Path(dir)
        gateway.get_ipfs_binary(ipfs_url, output_filepath)
        assert output_filepath.exists()
