import hashlib
import json
import pathlib
from typing import Protocol, Optional
from anv import models


def get_sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


class Respository(Protocol):
    def get_NFT_metadata(
        self, network: models.Network, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        pass

    def set_NFT_metadata(
        self, network: models.Network, data: models.NftMetadata
    ) -> bool:
        pass

    def get_klaytn_nft_contract(
        self, contract_address: str
    ) -> Optional[models.KlaytnNftContract]:
        pass

    def set_klaytn_nft_contract(self, nft_contract: models.KlaytnNftContract) -> bool:
        pass


class DiskRepository(Respository):
    def __init__(self):
        self.repo_dir = pathlib.Path(__file__).parent / ".data"

    def get_NFT_metadata(
        self, network: models.Network, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        json_filepath = self._get_json_filepath(network, contract_address, token_id)
        if not json_filepath.exists():
            return None
        result = models.NftMetadata.parse_file(json_filepath)
        result.cached = True
        return result

    def set_NFT_metadata(
        self,
        network: models.Network,
        data: models.NftMetadata,
    ) -> bool:
        json_filepath = self._get_json_filepath(
            network, data.contract_address, data.token_id
        )
        with json_filepath.open("w") as f:
            f.write(json.dumps(data.dict(), indent=4))
        return True

    def _get_json_filepath(
        self, network: models.Network, contract_address: str, token_id: str
    ):
        filename = get_sha256(f"{network.value}_{contract_address}_{token_id}")
        return self.repo_dir / f"{filename}.json"


class DBRepository(Respository):
    def get_NFT_metadata(
        self, network: models.Network, contract_address: str, token_id: str
    ) -> Optional[models.NftMetadata]:
        return None

    def set_NFT_metadata(
        self,
        network: models.Network,
        data: models.NftMetadata,
    ) -> bool:
        return True
