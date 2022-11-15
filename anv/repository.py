import os
import base64
import hashlib
import json
import logging
import pathlib
from typing import Protocol, Optional

import pymongo
from anv import models

log = logging.getLogger(f"anv.{__name__}")


def get_sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


class NFTMetadataRespository(Protocol):
    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        pass

    def set_NFT_metadata(self, network: models.Chain, data: models.NftMetadata) -> bool:
        pass


class NFTSourceRepository(Protocol):
    """NFT source(image, video) 를 caching 하는 저장소.
    NFT 의 token uri 값을 보내면 caching 된 URL(models.NftUrl) return
    """

    def get_nft_cached_urls(self, uri: str) -> models.NftUrl:
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
        network: models.Chain,
        data: models.NftMetadata,
    ) -> bool:
        json_filepath = self._get_json_filepath(
            network, data.contract_address, data.token_id
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
        network: models.Chain,
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

    def set_NFT_metadata(self, network: models.Chain, data: models.NftMetadata) -> bool:
        data.cached = True
        result = self.client.nft.metadata.find_one_and_replace(
            {
                "chain": network.value,
                "contract_address": data.contract_address,
                "token_id": data.token_id,
            },
            data.dict(),
        )
        if result is None:
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

    def get_nft_cached_urls(self, uri: str) -> models.NftUrl:
        new_uri = self._remove_quote_escape(uri)
        return models.NftUrl(original=new_uri)

    def _remove_quote_escape(self, uri: str):
        return uri
        # if uri.startswith("data:image/svg+xml;utf8,"):
        #     _, data = uri.split("data:image/svg+xml;utf8,")
        #     # _, base64_data = uri.split(",")
        #     encoded_data = base64.encode(data)
        #     # text = decoded_data.decode("utf-8")
        #     result = f"data:iamge/base64;utf8,{encoded_data}"

        #     # log.info(result)
        #     return uri
        # else:
        #     return uri


class GcpNFTSourceRepository(NFTSourceRepository):
    def get_nft_cached_urls(self, uri: str) -> models.NftUrl:
        return super().get_nft_cached_urls(uri)
