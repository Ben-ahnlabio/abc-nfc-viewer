import hashlib
import io
import json
import logging
import mimetypes
import os
import pathlib
from typing import Optional, Protocol
from urllib.parse import urljoin

import boto3
import magic
import mypy_boto3_s3
import pymongo
import requests
from google.cloud import storage
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from anv import models, aws_s3
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


class NFTSourceRepositoryProtocol(Protocol):
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
        # log.debug("set nft metadata data=%s", data)
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
        mongodb_uri = os.environ.get("MONGODB_URI_HOST")
        host = os.environ.get("MONGODB_HOST")
        user = os.environ.get("MONGODB_USER")
        password = os.environ.get("MONGODB_PASSWORD")
        ssl = os.environ.get("MONGODB_SSL") == "true"

        connection_string = f"{mongodb_uri}://{user}:{password}@{host}"
        return pymongo.MongoClient(
            connection_string, ssl=ssl, tlsAllowInvalidCertificates=True
        )


class DiskNFSSourceRepository(NFTSourceRepositoryProtocol):
    def __init__(self):
        self.repo_dir = pathlib.Path(__file__).parent / ".data"

    def cache_nft_source(self, nft: models.NftMetadata):
        pass

    def _remove_quote_escape(self, uri: str):
        return uri


class NFTSourceRepository(NFTSourceRepositoryProtocol):
    def __init__(self, repo: NFTMetadataRespository, ipfs: ipfs.IPFSProxy):
        self.repo = repo
        self.ipfs = ipfs

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


class AWSS3SourceRepository(NFTSourceRepository):
    def __init__(
        self,
        s3_storage: aws_s3.AWSS3Storage,
        repo: NFTMetadataRespository,
        ipfs: ipfs.IPFSProxy,
    ):
        self.repo = repo
        self.ipfs = ipfs
        self.s3_storage = s3_storage
        self.s3: mypy_boto3_s3.S3Client = boto3.client(
            service_name="s3",
            region_name=os.getenv("AWS_S3_REGION_NAME"),
            aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
        )
        self.bucket_name = os.environ["AWS_S3_BUCKET_NAME"]
        self.base_url = "https://abc-nft-source.s3.us-east-2.amazonaws.com/"
        self.resize_base_url = (
            "https://abc-nft-source-resized.s3.us-east-2.amazonaws.com/"
        )

    def cache_nft_source(self, nft: models.NftMetadata):
        """AWS S3 에 NFT source 를 저장."""
        uri = nft.image or nft.animation_url
        if not uri:
            return

        log.debug("cache nft source %s", nft)
        nft_url = self._cache_uri_source(uri)
        nft.source_url = nft_url
        nft.content_type = nft_url.content_type
        self.repo.set_NFT_metadata(nft)

    def _cache_uri_source(self, uri: str):
        """S3 에 저장 시 content_type 에 따른 확장자를 넣어야 함
        resize lambda function 에서는 파일의 내용을 참고하지 않고
        확장자만으로 content_type 을 결정함(mimetype 사용)
        """
        # surfix = ""  # AWS s3 의 key 에 들어갈 확장자
        uri_hash = get_sha256(uri)
        obj = self.s3_storage.find_first_object(uri_hash)

        # guess_extension 이 webp 확장자를 지원하지 않으므로 추가
        mimetypes.add_type("image/webp", ".webp")
        if obj:
            obj = self.s3_storage.get_object(obj["Key"])
            content_type = (
                obj.get("ResponseMetadata", {})
                .get("HTTPHeaders", {})
                .get("content-type")
            )
            surfix = mimetypes.guess_extension(str(content_type))
            if surfix is None:
                surfix = ""
        else:
            with io.BytesIO() as buffer:
                self._get_binary_from_uri(uri, buffer)
                buffer.seek(0)
                content_type = magic.from_buffer(buffer.read(), mime=True)
                surfix = mimetypes.guess_extension(str(content_type))
                if surfix is None:
                    surfix = ""
                new_key = f"{uri_hash}{surfix}"
                self._upload_object(buffer, new_key, content_type)

        nft_url = models.NftUrl(original=urljoin(self.base_url, f"{uri_hash}{surfix}"))
        # image 인 경우 lambda 에 의해 resize 되므로 resize url 추가
        if content_type and content_type.startswith("image/"):
            nft_url.h250 = urljoin(self.resize_base_url, f"{uri_hash}_h250{surfix}")
            nft_url.h500 = urljoin(self.resize_base_url, f"{uri_hash}_h500{surfix}")
            nft_url.h750 = urljoin(self.resize_base_url, f"{uri_hash}_h750{surfix}")
            nft_url.h1000 = urljoin(self.resize_base_url, f"{uri_hash}_h1000{surfix}")

        nft_url.content_type = content_type
        return nft_url

    def _upload_object(self, buffer, key: str, content_type: str):
        buffer.seek(0)
        self.s3_storage.upload_object(buffer, key, {"ContentType": content_type})
