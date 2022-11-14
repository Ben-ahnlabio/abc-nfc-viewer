from anv import api, repository
from anv.api import alchemy, kas, ipfs
from anv.service import (
    NFTService,
    KlaytnNFTService,
    EthereumNFTService,
    PolygonNFTService,
)


class AppConfig:
    def get_nft_service(self) -> NFTService:
        ethereum = self.get_ethereum_nft_service()
        polygon = self.get_polygon_nft_service()
        klaytn = self.get_klaytn_nft_service()
        repo = self.get_nft_src_repository()
        return NFTService(ethereum, polygon, klaytn, repo)

    def get_ethereum_nft_service(self) -> EthereumNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return EthereumNFTService(nft_metadata_repo, ipfs_proxy, alchemy_api)

    def get_polygon_nft_service(self) -> PolygonNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return PolygonNFTService(nft_metadata_repo, ipfs_proxy, alchemy_api)

    def get_klaytn_nft_service(self) -> KlaytnNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        klaytn_api = self.get_kas_api()
        return KlaytnNFTService(nft_metadata_repo, ipfs_proxy, klaytn_api)

    def get_ethereum_api(self) -> api.EthereumApi:
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return api.EthereumApi(repo, ipfs, alchemy_api)

    def get_klaytn_api(self) -> api.KlaytnApi:
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_proxy()
        kas_api = self.get_kas_api()
        return api.KlaytnApi(repo, ipfs, kas_api)

    def get_polyfon_api(self) -> api.PolygonApi:
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return api.PolygonApi(repo, ipfs, alchemy_api)

    def get_ipfs_proxy(self) -> ipfs.IPFSProxy:
        return ipfs.IPFSProxy()

    def get_kas_api(self) -> kas.KasApi:
        return kas.KasApi()

    def get_nft_meta_repository(self) -> repository.DiskRepository:
        return repository.DiskRepository()

    def get_nft_src_repository(self) -> repository.DiskNFSSourceRepository:
        return repository.DiskNFSSourceRepository()

    def get_alchemy_api(self) -> alchemy.AlchemyApi:
        return alchemy.AlchemyApi()
