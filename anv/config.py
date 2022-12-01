from anv import models, repository, aws_s3
from anv.api import alchemy, kas, ipfs, moralis
from anv.service import (
    BinanceNFTService,
    BinanceTestNFTService,
    KlaytnBaobobNFTService,
    NFTService,
    KlaytnNFTService,
    EthereumNFTService,
    PolygonMumbaiNFTService,
    PolygonNFTService,
    EthereumGoerliNFTService,
)


class AppConfig:
    def __init__(self):
        self._ipfs = None
        self._nft_meta_repo = None
        self._nft_src_repo = None

    def get_nft_service(self) -> NFTService:
        chains = {
            models.Chain.ETHEREUM.value: self.get_ethereum_nft_service(),
            models.Chain.POLYGON.value: self.get_polygon_nft_service(),
            models.Chain.KLAYTN.value: self.get_klaytn_nft_service(),
            models.Chain.BINANCE.value: self.get_binance_nft_service(),
            models.Chain.ETHEREUM_GOERLI.value: self.get_ethereum_goerli_nft_service(),
            models.Chain.POLYGON_MUMBAI.value: self.get_polygon_mumbai_nft_service(),
            models.Chain.BINANCE_TESTNET.value: self.get_binance_test_nft_service(),
            models.Chain.KLAYTN_BAOBAB.value: self.get_klaytn_baobob_nft_service(),
        }
        return NFTService(**chains)

    def get_ethereum_nft_service(self) -> EthereumNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return EthereumNFTService(nft_metadata_repo, ipfs_proxy, alchemy_api)

    def get_ethereum_goerli_nft_service(self) -> EthereumGoerliNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return EthereumGoerliNFTService(nft_metadata_repo, ipfs_proxy, alchemy_api)

    def get_polygon_nft_service(self) -> PolygonNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return PolygonNFTService(nft_metadata_repo, ipfs_proxy, alchemy_api)

    def get_polygon_mumbai_nft_service(self) -> PolygonMumbaiNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        alchemy_api = self.get_alchemy_api()
        return PolygonMumbaiNFTService(nft_metadata_repo, ipfs_proxy, alchemy_api)

    def get_klaytn_nft_service(self) -> KlaytnNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        klaytn_api = self.get_kas_api()
        return KlaytnNFTService(nft_metadata_repo, ipfs_proxy, klaytn_api)

    def get_klaytn_baobob_nft_service(self) -> KlaytnBaobobNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        klaytn_api = self.get_kas_api()
        return KlaytnBaobobNFTService(nft_metadata_repo, ipfs_proxy, klaytn_api)

    def get_binance_nft_service(self) -> BinanceNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        moralis_api = self.get_moralis_api()
        return BinanceNFTService(nft_metadata_repo, ipfs_proxy, moralis_api)

    def get_binance_test_nft_service(self) -> BinanceTestNFTService:
        nft_metadata_repo = self.get_nft_meta_repository()
        ipfs_proxy = self.get_ipfs_proxy()
        moralis_api = self.get_moralis_api()
        return BinanceTestNFTService(nft_metadata_repo, ipfs_proxy, moralis_api)

    def get_ipfs_proxy(self) -> ipfs.IPFSProxy:
        if self._ipfs:
            return self._ipfs
        self._ipfs = ipfs.IPFSProxy()
        return self._ipfs

    def get_nft_meta_repository(self) -> repository.NFTMetadataRespository:
        if self._nft_meta_repo:
            return self._nft_meta_repo
        self._nft_meta_repo = repository.MongodbRepository()
        return self._nft_meta_repo

    def get_nft_src_repository(self) -> repository.NFTSourceRepositoryProtocol:
        if self._nft_src_repo:
            return self._nft_src_repo

        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_proxy()
        s3_storage = aws_s3.AWSS3Storage()

        self._nft_src_repo = repository.AWSS3SourceRepository(s3_storage, repo, ipfs)
        return self._nft_src_repo

    def get_alchemy_api(self) -> alchemy.AlchemyApi:
        return alchemy.AlchemyApi()

    def get_moralis_api(self) -> moralis.MorailsApi:
        return moralis.MorailsApi()

    def get_kas_api(self) -> kas.KasApi:
        return kas.KasApi()
