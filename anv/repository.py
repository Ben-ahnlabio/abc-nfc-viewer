import hashlib
import io
import json
import logging
import os
import pathlib
from typing import Optional, Protocol

import magic
import pymongo
import requests
from google.cloud import storage
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from anv import models
from anv.api import ipfs

log = logging.getLogger(f"anv.{__name__}")


def get_sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


class NFTMetadataRespository(Protocol):
    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        """cache 된 nft metadata 를 repository 로부터 받아온다.
        cache 데이터가 없으면 return None.
        """

    def set_NFT_metadata(self, data: models.NftMetadata) -> bool:
        """nft metadata 를 저장한다.
        이미 존재하는 nft metadata 인 경우 chain, contract_address, token_id 기준으로 기존 데이터를 덮어쓴다.
        """


class NFTSourceRepository(Protocol):
    """NFT source(image, video) 를 caching 하는 저장소.
    NFT 의 token uri 값을 보내면 caching 된 URL(models.NftUrl) return
    """

    def cache_nft_source(self, nft: models.NftMetadata):
        pass


class DiskRepository(NFTMetadataRespository):
    """NFT metadat 를 disk 에 caching 한다. test 용"""

    def __init__(self):
        self.repo_dir = pathlib.Path(__file__).parent / ".data"

    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        json_filepath = self._get_json_filepath(network, contract_address, token_id)
        if not json_filepath.exists():
            return None
        result = models.NftMetadata.parse_file(json_filepath)
        result.cached = True
        return result

    def set_NFT_metadata(
        self,
        data: models.NftMetadata,
    ) -> bool:
        json_filepath = self._get_json_filepath(
            models.Chain(data.chain), data.contract_address, data.token_id
        )

        if not json_filepath.parent.exists():
            json_filepath.parent.mkdir()

        with json_filepath.open("w") as f:
            f.write(json.dumps(data.dict(), indent=4))
        return True

    def _get_json_filepath(
        self, network: models.Chain, contract_address: str, token_id: str
    ):
        filename = get_sha256(f"{network.value}_{contract_address}_{token_id}")
        return self.repo_dir / pathlib.Path(network.value) / f"{filename}.json"


class DBRepository(NFTMetadataRespository):
    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        return None

    def set_NFT_metadata(
        self,
        data: models.NftMetadata,
    ) -> bool:
        return True


class MongodbRepository(NFTMetadataRespository):
    def __init__(self):
        self.client = self._get_mongo_client()

    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        result = self.client.nft.metadata.find_one(
            {
                "chain": network.value,
                "contract_address": contract_address,
                "token_id": token_id,
            }
        )
        if result is None:
            return None

        return models.NftMetadata.parse_obj(result)

    def set_NFT_metadata(self, data: models.NftMetadata) -> bool:
        log.debug("set nft metadata data=%s", data)
        data.cached = True
        result = self.client.nft.metadata.find_one_and_replace(
            {
                "chain": data.chain,
                "contract_address": data.contract_address,
                "token_id": data.token_id,
            },
            data.dict(),
        )
        if result is None:
            log.debug("data not exists. insert data=%s", data)
            result = self.client.nft.metadata.insert_one(data.dict())
        return True

    def _get_mongo_client(self) -> pymongo.MongoClient:
        host = os.environ.get("MONGODB_HOST")
        user = os.environ.get("MONGODB_USER")
        password = os.environ.get("MONGODB_PASSWORD")

        connection_string = f"mongodb+srv://{user}:{password}@{host}"
        return pymongo.MongoClient(
            connection_string, ssl=True, tlsAllowInvalidCertificates=True
        )


class DiskNFSSourceRepository(NFTSourceRepository):
    def __init__(self):
        self.repo_dir = pathlib.Path(__file__).parent / ".data"

    def cache_nft_source(self, nft: models.NftMetadata):
        pass

    def _remove_quote_escape(self, uri: str):
        return uri


class GcpNFTSourceRepository(NFTSourceRepository):
    def __init__(self, repo: NFTMetadataRespository, ipfs: ipfs.IPFSProxy):
        self.repo = repo
        self.ipfs = ipfs
        self.storage = storage.Client()
        self.bucket = self.storage.bucket("nft_source")

    def store_nft_source(self, uri, uri_hash):
        with io.BytesIO() as buffer:
            self._get_binary_from_uri(uri, buffer)
            original_name = f"{uri_hash}_original"
            return self._upload_blob(buffer, original_name)

    def cache_nft_source(self, nft: models.NftMetadata):
        uri = nft.image or nft.animation_url
        if not uri:
            return

        log.debug("cache nft source %s", nft)
        uri_hash = get_sha256(uri)
        original_name = f"{uri_hash}_original"
        blob = self.bucket.get_blob(original_name)
        if blob:
            log.debug("blob exists. update nft url %s", blob.public_url)
            nft.source_url = models.NftUrl(original=blob.public_url)
        else:
            log.debug("blob not exists. store_nft_source. uri=%s", uri)
            blob = self.store_nft_source(uri, uri_hash)
            if blob:
                nft.source_url = models.NftUrl(original=blob.public_url)

        nft.content_type = blob.content_type
        self.repo.set_NFT_metadata(nft)

    def _upload_blob(self, file_obj, destination_blob_name):
        """Uploads a file to the bucket."""

        blob = self.bucket.blob(destination_blob_name)
        file_obj.seek(0)
        content_type = magic.from_buffer(file_obj.read(), mime=True)
        log.debug("uploading blob...")
        blob.upload_from_file(file_obj, rewind=True, content_type=content_type)

        log.debug(
            "[UPLOADED] File blob_name=%s content_type=%s",
            destination_blob_name,
            content_type,
        )

        return blob

    def _get_binary_from_uri(
        self, uri: str, buffer: io.BytesIO
    ) -> Optional[io.BytesIO]:
        if uri.startswith("http"):
            return self._get_binary_from_http(uri, buffer)
        elif uri.startswith("ipfs://"):
            return self._get_binary_from_ipfs(uri, buffer)
        elif uri.startswith("data:image/svg+xml;utf8"):
            return self._get_binary_from_raw_data(uri, buffer)
        else:
            return None

    def _get_binary_from_ipfs(
        self, ipfs_url: str, buffer: io.BytesIO
    ) -> Optional[io.BytesIO]:
        return self.ipfs.get_ipfs_binary(ipfs_url, buffer)

    def _get_binary_from_http(
        self, uri: str, buffer: io.BytesIO
    ) -> Optional[io.BytesIO]:
        try:
            log.debug("getting binary from uri... %s", uri)
            r = requests.get(uri, timeout=5)
            r.raise_for_status()
            for chunk in r.iter_content(1024 * 1024):
                buffer.write(chunk)
            return buffer
        except Exception as e:
            log.error("requests error. %s uri=%s.", e, uri)

        if "ipfs/" not in uri:
            return None

        buffer.seek(0)
        buffer.truncate(0)
        return self.ipfs.get_binary_from_http_url(uri, buffer)

    def _get_binary_from_raw_data(
        self, uri: str, buffer: io.BytesIO
    ) -> Optional[io.BytesIO]:
        _, data = uri.split(",")

        with io.StringIO() as data_buffer:
            data_buffer.write(data)
            data_buffer.seek(0)
            drawing = svg2rlg(data_buffer)
            renderPM.drawToFile(drawing, buffer, dpi=72 * 10, fmt="PNG")
