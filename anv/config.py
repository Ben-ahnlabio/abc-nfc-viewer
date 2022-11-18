from anv import repository
from anv.api import alchemy, kas, ipfs, moralis
from anv.service import (
    BinanceNFTService,
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
        binance = self.get_binance_nft_service()
        repo = self.get_nft_src_repository()
        return NFTService(
            ethereum=ethereum,
            polygon=polygon,
            klaytn=klaytn,
            binance=binance,
            repo=repo,
        )

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

    def get_binance_nft_service(self) -> BinanceNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        moralis_api = self.get_moralis_api()
        return BinanceNFTService(nft_metadata_repo, ipfs_proxy, moralis_api)

    def get_ipfs_proxy(self) -> ipfs.IPFSProxy:
        return ipfs.IPFSProxy()

    def get_kas_api(self) -> kas.KasApi:
        return kas.KasApi()

    def get_nft_meta_repository(self) -> repository.NFTMetadataRespository:
        return repository.DiskRepository()
        # return repository.MongodbRepository()

    def get_nft_src_repository(self) -> repository.NFTSourceRepository:
        # return repository.DiskNFSSourceRepository()
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_proxy()
        return repository.GcpNFTSourceRepository(repo, ipfs)

    def get_alchemy_api(self) -> alchemy.AlchemyApi:
        return alchemy.AlchemyApi()

    def get_moralis_api(self) -> moralis.MorailsApi:
        return moralis.MorailsApi()
