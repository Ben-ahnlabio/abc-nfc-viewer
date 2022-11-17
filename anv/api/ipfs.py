import json
import logging
import pathlib
import io
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

    def get_json(self, ipfs_uri: str) -> dict:
        with io.BytesIO() as buffer:
            self.get_ipfs_binary(ipfs_uri, buffer)
            buffer.seek(0)
            data = buffer.read()
            return json.loads(data)

    def get_ipfs_binary(self, ipfs_uri: str, buffer: io.BytesIO) -> io.BytesIO:
        from_ipfs = ipfs_uri.replace("ipfs://", "")
        download_urls = [urljoin(gateway, from_ipfs) for gateway in self.gp_urls]

        for url in download_urls:
            try:
                return self._get_binaray(url, buffer)
            except Exception as e:
                # 예외발생 시 buffer 비움
                buffer.seek(0)
                buffer.truncate(0)
                log.warning("ipfs download error. %s", e)

        raise IPFSDownloadError("ipfs download error.", ipfs_uri)

    def get_binary_from_http_url(self, url: str, buffer: io.BytesIO):
        _, path = url.split("ipfs/")
        ipfs_url = f"ipfs://{path}"
        return self.get_ipfs_binary(ipfs_url, buffer)

    def _get_binaray(self, url: str, buffer: io.BytesIO) -> io.BytesIO:
        log.debug("downloading... url=%s", url)
        r = requests.get(url, timeout=1)
        r.raise_for_status()

        for chunk in r.iter_content(1024 * 1024):
            buffer.write(chunk)
        log.debug("download done... url=%s", url)
        return buffer
