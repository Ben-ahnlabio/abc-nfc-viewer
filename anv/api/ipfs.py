import json
import logging
import pathlib
import tempfile
from urllib.parse import urljoin

import requests

log = logging.getLogger(f"anv.{__name__}")


class IPFSError(Exception):
    pass


class IPFSDownloadError(IPFSError):
    pass


class IPFSProxy:
    def __init__(self):
        self.gp_urls = [
            "https://ipfs.io/ipfs/",
            "https://dweb.link/ipfs/",
            "https://gateway.ipfs.io/ipfs/",
            "https://cloudflare-ipfs.com/ipfs/",
        ]

    def get_json(self, ipfs_uri: str):
        with tempfile.TemporaryDirectory() as dir:
            json_file = self.get_ipfs_binary(ipfs_uri, pathlib.Path(dir))
            with json_file.open("r") as f:
                return json.loads(f.read())

    def get_ipfs_binary(self, ipfs_uri: str, output_dir: pathlib.Path) -> pathlib.Path:
        ipfs_path = ipfs_uri.replace("ipfs://", "")
        download_urls = [urljoin(gateway, ipfs_path) for gateway in self.gp_urls]

        for url in download_urls:
            try:
                return self._get_binaray(url, output_dir)
            except Exception as e:
                log.warning("ipfs download error. %s", e)

        raise IPFSDownloadError("ipfs download error.", ipfs_uri)

    def _get_binaray(self, url: str, tmp_dir: pathlib.Path) -> pathlib.Path:
        log.debug("downloading... url=%s", url)
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        with tempfile.NamedTemporaryFile("wb", dir=tmp_dir, delete=False) as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)
        log.debug("download done... url=%s path=%s", url, f.name)
        return pathlib.Path(f.name)
