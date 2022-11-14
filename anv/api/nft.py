import logging
from typing import List

from anv import models
from anv.api import alchemy
from anv.repository import NFSMetadataRespository

log = logging.getLogger(f"anv.{__name__}")


class NftApi:
    def __init__(self, repo: NFSMetadataRespository, alchemy: alchemy.AlchemyApi):
        self.alchemy = alchemy
        self.repo = repo

    def get_ethereum_nfts(
        self, owner: str, resync: bool = False
    ) -> List[models.NftMetadata]:
        """ether wallet address 로부터 ethereum nft 데이터를 가져온다.
        alchemy api 를 사용해서 wallet 의 nft 를 가져온다.

        repository 로부터 caching nft metadata 데이터를 가져오고 없으면 alchemy api 를 호출한다.

        resync = False 인 경우 repository cache data 사용,
        resync = True 인 경우 repository cache data 를 사용하지 않고 API 데이터로 갱신함.

        Args:
            owner: wallet address
            resync: repository 데이터 사용
        """
        owned_nfts = self.alchemy.get_NFTs(alchemy.AlchemyNet.EthMainNet, owner)
        if resync:
            nft_metadata_list = [
                self._get_ethereum_nft_metadata_from_api(nft) for nft in owned_nfts
            ]
            [self._store_ethereum_metadata(nft) for nft in nft_metadata_list]
            return nft_metadata_list

        return [self._get_ethereum_nft_metadata(nft) for nft in owned_nfts]

    def _get_ethereum_nft_metadata(self, nft: alchemy.AlchemyOwnedNft):
        metadata = self.repo.get_NFT_metadata(
            models.Chain.ETHEREUM, nft.contract_address, nft.token_id
        )
        if metadata:
            return metadata
        if metadata is None:
            metadata = self.alchemy.get_NFT_metadata(
                alchemy.AlchemyNet.EthMainNet, nft.contract_address, nft.token_id
            )
            self._store_ethereum_metadata(nft)
            return metadata

    def _get_ethereum_nft_metadata_from_api(self, nft: alchemy.AlchemyOwnedNft):
        return alchemy.AlchemyNet.EthMainNet, nft.contract_address, nft.token_id

    def _store_ethereum_metadata(self, nft: alchemy.AlchemyOwnedNft):
        pass

    def get_klaytn_nfts(self, owner: str) -> List[models.NftMetadata]:
        pass

    def get_polygon_nfts(self, owner: str) -> List[models.NftMetadata]:
        pass

    def get_binance_nfts(self, owner: str) -> List[models.NftMetadata]:
        pass
