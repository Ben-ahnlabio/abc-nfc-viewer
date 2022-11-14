from anv import api, repository
from anv.api import alchemy, kas, ipfs


class AppConfig:
    def get_ethereum_api(self) -> api.EthereumApi:
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_gateway()
        alchemy_api = self.get_alchemy_api()
        return api.EthereumApi(repo, ipfs, alchemy_api)

    def get_klaytn_api(self) -> api.KlaytnApi:
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_gateway()
        kas_api = self.get_kas_api()
        return api.KlaytnApi(repo, ipfs, kas_api)

    def get_polyfon_api(self) -> api.PolygonApi:
        repo = self.get_nft_meta_repository()
        ipfs = self.get_ipfs_gateway()
        alchemy_api = self.get_alchemy_api()
        return api.PolygonApi(repo, ipfs, alchemy_api)

    def get_ipfs_gateway(self) -> ipfs.IPFSGateway:
        return ipfs.IPFSGateway()

    def get_kas_api(self) -> kas.KasApi:
        return kas.KasApi()

    def get_nft_meta_repository(self) -> repository.DiskRepository:
        return repository.DiskRepository()

    def get_nft_src_repository(self) -> repository.DiskNFSSourceRepository:
        return repository.DiskNFSSourceRepository()

    def get_alchemy_api(self) -> alchemy.AlchemyApi:
        return alchemy.AlchemyApi()
