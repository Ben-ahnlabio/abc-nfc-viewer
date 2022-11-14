import base64
import hashlib
import json
import logging
import pathlib
from typing import Protocol, Optional
from anv import models

log = logging.getLogger(f"anv.{__name__}")


def get_sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


class NFSMetadataRespository(Protocol):
    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        pass

    def set_NFT_metadata(self, network: models.Chain, data: models.NftMetadata) -> bool:
        pass


class NFTSourceRepository(Protocol):
    def get_nft_cached_urls(self, uri: str) -> models.NftUrl:
        pass


class DiskRepository(NFSMetadataRespository):
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


class DBRepository(NFSMetadataRespository):
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


class DiskNFSSourceRepository(NFTSourceRepository):
    def __init__(self):
        self.repo_dir = pathlib.Path(__file__).parent / ".data"

    def get_nft_cached_urls(self, uri: str) -> models.NftUrl:
        new_uri = self._remove_quote_escape(uri)
        return models.NftUrl(original=new_uri)

    def _remove_quote_escape(self, uri: str):
        if uri.startswith("data:image/svg+xml;utf8,"):
            _, data = uri.split("data:image/svg+xml;utf8,")
            # _, base64_data = uri.split(",")
            encoded_data = base64.encode(data)
            # text = decoded_data.decode("utf-8")
            result = f"data:iamge/base64;utf8,{encoded_data}"

            # log.info(result)
            return uri
        else:
            return uri
