import hashlib
import json
import pathlib
from typing import List, Protocol, Optional
from anv import models


def get_sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


class NFSMetadataRespository(Protocol):
    def get_NFT_metadata(
        self, network: models.Chain, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        pass

    def set_NFT_metadata(self, network: models.Chain, data: models.NftMetadata) -> bool:
        pass


class NFSSourceRepository(Protocol):
    def get_nft_cached_urls(self, nfs_url: str) -> models.NftUrl:
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


class DiskNFSSourceRepository(NFSSourceRepository):
    def __init__(self):
        self.repo_dir = pathlib.Path(__file__).parent / ".data"

    def get_nft_cached_urls(self, uri: Optional[str]) -> models.NftUrl:
        if not uri:
            return None
        return models.NftUrl(original=uri)
