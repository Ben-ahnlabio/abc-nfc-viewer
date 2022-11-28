import base64
from concurrent import futures
import json
import logging
from typing import List, Optional, Protocol, TypedDict
import pydantic

import requests

from anv import models, repository
from anv.api import alchemy, kas, moralis, ipfs

log = logging.getLogger(f"anv.{__name__}")

MAX_WORKERS = 5


class NFTAttribute(TypedDict):
    display_type: Optional[str]
    trait_type: str
    value: str


class NFTTokenJson(TypedDict):
    name: str
    image: Optional[str]
    description: Optional[str]
    attributes: List[NFTAttribute]
    url: Optional[str]
    external_url: Optional[str]
    external_uri: Optional[str]


class OwnedNftResult(pydantic.BaseModel):
    cursor: Optional[str]
    nfts: List[models.NftMetadata]


class NFTServiceProtocol(Protocol):
    def get_NFTs_by_owner(
        self, owner: str, cursor: str = None, resync: bool = False
    ) -> OwnedNftResult:
        pass

    def get_NFT_by_contract_token_id(
        self, contract_address: str, token_id: str, resync: bool
    ) -> Optional[models.NftMetadata]:
        pass


class NFTServiceBase(NFTServiceProtocol):
    def __init__(self, ipfs: ipfs.IPFSProxy):
        self.ipfs = ipfs

    def _get_token_data_by_uri(self, uri: str) -> NFTTokenJson:
        """uri 에 따른 데이터 parsing

        data:application/json;base64,
        data:image/svg+xml;utf8,
        http://
        ipfs://

        """

        if uri.startswith("ipfs://"):
            return self.ipfs.get_json(uri)
        elif uri.startswith("data:application/json;base64"):
            return self._get_base_64_json(uri)
        else:  # http
            return self._get_json_from_http(uri)

    def _get_base_64_json(self, uri: str) -> NFTTokenJson:
        _, base64_data = uri.split(",")
        decoded_data = base64.b64decode(base64_data)
        text = decoded_data.decode("utf-8")
        return json.loads(text)

    def _get_json_from_http(self, uri: str) -> NFTTokenJson:
        r = requests.get(uri, timeout=5, verify=False)
        r.raise_for_status()
        return r.json()


class AlchemyBaseNFTService(NFTServiceBase):
    def __init__(
        self,
        repo: repository.NFTMetadataRespository,
        ipfs: ipfs.IPFSProxy,
        alchemy_api: alchemy.AlchemyApi,
    ):
        self.alchemy_api = alchemy_api
        self.repo = repo
        self.ipfs = ipfs
        self.network: alchemy.AlchemyNet
        self.net_map = {
            alchemy.AlchemyNet.EthMainNet.value: models.Chain.ETHEREUM,
            alchemy.AlchemyNet.PolygonMainNet.value: models.Chain.POLYGON,
        }

    def get_NFTs_by_owner(
        self, owner: str, cursor: str = None, resync: bool = False
    ) -> OwnedNftResult:
        """ether wallet address 로부터 ethereum nft 데이터를 가져온다.
        alchemy api 를 사용해서 wallet 의 nft 를 가져온다.

        repository 로부터 caching nft metadata 데이터를 가져오고 없으면 alchemy api 를 호출한다.

        resync = False 인 경우 repository cache data 사용,
        resync = True 인 경우 repository cache data 를 사용하지 않고 API 데이터 return, repository 를 갱신함.

        Args:
            owner: wallet address
            resync: repository 데이터 사용
        """
        owned_nfts_result = self.alchemy_api.get_NFTs(self.network, owner, cursor)
        with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as exec:
            if resync:
                future_list = [
                    exec.submit(self._get_nft_metadata_from_api, nft)
                    for nft in owned_nfts_result.owned_nfts
                ]
            else:
                future_list = [
                    exec.submit(self._get_nft_metadata, nft)
                    for nft in owned_nfts_result.owned_nfts
                ]
            result = [f.result() for f in future_list]

        return OwnedNftResult(
            cursor=owned_nfts_result.cursor,
            nfts=[nft for nft in result if nft is not None],
        )

    def get_NFT_by_contract_token_id(
        self, contract_address: str, token_id: str, resync: bool
    ):
        if resync:
            nft = alchemy.AlchemyOwnedNft(
                contract_address=contract_address, token_id=token_id
            )
            return self._get_nft_metadata_from_api(nft)
        else:
            return self.repo.get_NFT_metadata(
                self.net_map[self.network.value], contract_address, token_id
            )

    def _get_nft_metadata_from_api(
        self, nft: alchemy.AlchemyOwnedNft
    ) -> Optional[models.NftMetadata]:
        try:
            nft_metadata = self.alchemy_api.get_NFT_metadata(
                self.network, nft.contract_address, nft.token_id
            )

            # NFT metadata 를 repository 에 caching
            self.repo.set_NFT_metadata(nft_metadata)
            return nft_metadata
        except Exception as e:
            log.error("get_nft_metadata_from_api error. %s nft=%s", e, nft)
            return None

    def _get_nft_metadata(
        self, nft: alchemy.AlchemyOwnedNft
    ) -> Optional[models.NftMetadata]:
        metadata = self.repo.get_NFT_metadata(
            self.net_map[self.network.value], nft.contract_address, nft.token_id
        )
        if metadata:
            return metadata
        return self._get_nft_metadata_from_api(nft)


class EthereumNFTService(AlchemyBaseNFTService):
    def __init__(
        self,
        repo: repository.NFTMetadataRespository,
        ipfs: ipfs.IPFSProxy,
        alchemy_api: alchemy.AlchemyApi,
    ):
        super().__init__(repo, ipfs, alchemy_api)
        self.network = alchemy.AlchemyNet.EthMainNet


class PolygonNFTService(AlchemyBaseNFTService):
    def __init__(
        self,
        repo: repository.NFTMetadataRespository,
        ipfs: ipfs.IPFSProxy,
        alchemy_api: alchemy.AlchemyApi,
    ):
        super().__init__(repo, ipfs, alchemy_api)
        self.network = alchemy.AlchemyNet.PolygonMainNet


class KlaytnNFTService(NFTServiceBase):
    def __init__(
        self,
        repo: repository.NFTMetadataRespository,
        ipfs: ipfs.IPFSProxy,
        kas: kas.KasApi,
    ):
        self.kas = kas
        self.repo = repo
        self.ipfs = ipfs

    def get_NFTs_by_owner(
        self, owner: str, cursor: str = None, resync: bool = False
    ) -> OwnedNftResult:
        owned_nfts_result = self.kas.get_tokens_by_owner(
            kas.ChainId.Cypress, owner, (kas.TokenKind.NFT, kas.TokenKind.MT), cursor
        )

        with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as exec:
            if resync:
                future_list = [
                    exec.submit(self._get_nft_metadata_from_api, nft)
                    for nft in owned_nfts_result.owned_nfts
                ]
            else:
                future_list = [
                    exec.submit(self._get_nft_metadata, nft)
                    for nft in owned_nfts_result.owned_nfts
                ]
            result = [f.result() for f in future_list]
        return OwnedNftResult(
            cursor=owned_nfts_result.cursor,
            nfts=[nft for nft in result if nft is not None],
        )

    def get_NFT_by_contract_token_id(
        self, contract_address: str, token_id: str, resync: bool
    ) -> Optional[models.NftMetadata]:
        if resync:
            owned_nft = kas.KlaytnOwnedNft(
                contract_address=contract_address, token_id=token_id
            )
            return self._get_nft_metadata_from_api(owned_nft)
        else:
            nft_metadata = self.repo.get_NFT_metadata(
                models.Chain.KLAYTN, contract_address, token_id
            )
            return nft_metadata

    def _get_nft_metadata_from_api(
        self, nft: kas.KlaytnOwnedNft
    ) -> Optional[models.NftMetadata]:
        """cache repository 를 거지치 않고 api 를 사용하여 nft metadata 를 생성한다.

        특정 nft 의 token uri 가 '' 값으로 출력되는 경우가 있음.
        metadata update API 를 호출하여 metadata update 요청
        """
        try:
            # nft metadata update
            self.kas.update_nft_token_metadata(
                kas.ChainId.Cypress, nft.contract_address, nft.token_id
            )
        except Exception as e:
            log.warning(
                "klaytn update_nft_token_metadata error. %s. contract_address=%s token_id=%s",
                e,
                nft.contract_address,
                nft.token_id,
            )

        try:
            nft_contract = self._get_nft_contract(nft.contract_address)
            if nft.token_uri:
                token_data = self._get_nft_by_token_uri(nft.token_uri)
            else:
                nft_result = self.kas.get_nft(
                    kas.ChainId.Cypress, nft.contract_address, nft.token_id
                )
                token_uri = nft_result["tokenUri"]
                token_data = self._get_nft_by_token_uri(token_uri)

        except Exception as e:
            log.error(
                "klaytn nft token uri source error. %s. contract_address=%s, token_id=%s",
                nft.token_uri,
                nft.contract_address,
                nft.token_id,
                extra={
                    "owner": nft.owner,
                    "contract_address": nft.contract_address,
                    "token_id": nft.token_id,
                    "token_uri": nft.token_uri,
                    "error": e,
                },
            )
            return None

        nft_metadata = models.NftMetadata(
            chain=models.Chain.KLAYTN.value,
            contract_address=nft.contract_address,
            contract_name=nft_contract.name,
            token_id=nft.token_id,
            token_type=nft_contract.type,
            name=token_data["name"],
            image=token_data["image"],
            animation_url=token_data.get("animation_url"),
            description=token_data.get("description"),
            attributes=[
                models.NftAttribute(
                    trait_type=attr["trait_type"],
                    value=attr["value"],
                    display_type=attr.get("display_type"),
                )
                for attr in token_data.get("attributes", [])
            ],
            external_url=token_data.get("external_url"),
            token_data=token_data,
        )
        self.repo.set_NFT_metadata(nft_metadata)
        return nft_metadata

    def _get_nft_metadata(
        self, nft: kas.KlaytnOwnedNft
    ) -> Optional[models.NftMetadata]:
        nft_metadata = self.repo.get_NFT_metadata(
            models.Chain.KLAYTN, nft.contract_address, nft.token_id
        )
        if nft_metadata:
            return nft_metadata

        return self._get_nft_metadata_from_api(nft)

    def _get_nft_by_token_uri(self, uri: str) -> NFTTokenJson:
        """uri 에 따른 데이터 parsing

        data:application/json;base64,
        data:image/svg+xml;utf8,
        http://
        ipfs://

        """

        if uri.startswith("ipfs://"):
            return self.ipfs.get_json(uri)
        elif uri.startswith("data:application/json;base64"):
            return self._get_base_64_json(uri)
        else:  # http
            return self._get_json_from_http(uri)

    def _get_base_64_json(self, uri: str) -> NFTTokenJson:
        _, base64_data = uri.split(",")
        decoded_data = base64.b64decode(base64_data)
        text = decoded_data.decode("utf-8")
        return json.loads(text)

    def _get_json_from_http(self, uri: str) -> NFTTokenJson:
        r = requests.get(uri, timeout=1, verify=False)
        r.raise_for_status()
        return r.json()

    def _get_nft_contract(self, contract_address: str) -> models.KlaytnNftContract:
        result = self.kas.get_nft_contract_raw(kas.ChainId.Cypress, contract_address)
        return models.KlaytnNftContract(
            address=result["address"],
            name=result["name"],
            symbol=result["symbol"],
            logo=result["logo"],
            total_supply=result["totalSupply"],
            status=result["status"],
            type=result["type"],
            created_at=result["createdAt"],
            updated_at=result["updatedAt"],
            deleted_at=result["deletedAt"],
            cached=False,
        )


class BinanceNFTService(NFTServiceBase):
    def __init__(
        self,
        repo: repository.NFTMetadataRespository,
        ipfs: ipfs.IPFSProxy,
        moralis_api: moralis.MorailsApi,
    ):
        self.moralis_api = moralis_api
        self.repo = repo
        self.ipfs = ipfs

    def get_NFTs_by_owner(
        self, owner: str, cursor: str = None, resync: bool = False
    ) -> OwnedNftResult:

        owned_nfts_result = self.moralis_api.get_NFTs(
            moralis.MorailsNetwork.BinanceMainNet, owner, cursor
        )

        result = []
        for nft in owned_nfts_result.owned_nfts:
            if resync:
                metadata = self._get_nft_metadata_from_api(nft)
            else:
                metadata = self._get_nft_metadata(nft)
            result.append(metadata)

        # multithread 실행 시 moralis API 가 Too many request 발생함
        # with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as exec:
        #     if resync:
        #         future_list = [
        #             exec.submit(self._get_nft_metadata_from_api, nft)
        #             for nft in owned_nfts_result.owned_nfts
        #         ]
        #     else:
        #         future_list = [
        #             exec.submit(self._get_nft_metadata, nft)
        #             for nft in owned_nfts_result.owned_nfts
        #         ]
        #     result = [f.result() for f in future_list]

        return OwnedNftResult(
            cursor=owned_nfts_result.cursor,
            nfts=[nft for nft in result if nft is not None],
        )

    def get_NFT_by_contract_token_id(
        self, contract_address: str, token_id: str, resync: bool
    ) -> Optional[models.NftMetadata]:

        nft = moralis.MoralisOwnedNft(token_address=contract_address, token_id=token_id)
        if resync:
            return self._get_nft_metadata_from_api(nft)
        else:
            return self.repo.get_NFT_metadata(
                models.Chain.BINANCE, nft.token_address, nft.token_id
            )

    def _get_nft_metadata_from_api(
        self, nft: moralis.MoralisOwnedNft
    ) -> models.NftMetadata:
        nft_metadata = self.moralis_api.get_NFT_metadata(
            moralis.MorailsNetwork.BinanceMainNet, nft.token_address, nft.token_id
        )

        token_data = self._get_token_data(nft_metadata)

        name = token_data.get("name")
        if not name:
            log.warning(
                "nft name not exist. contract_address=%s, token_id=%s",
                nft.token_address,
                nft.token_id,
            )
            name = nft_metadata.name

        attributes = []
        for attr in token_data.get("attributes", []):
            try:
                attributes.append(
                    models.NftAttribute(
                        trait_type=attr["trait_type"],
                        value=attr["value"],
                        display_type=attr.get("display_type"),
                    )
                )
            except (TypeError, KeyError) as e:
                log.warning(
                    "[Binance] NftMetadata attribute parse error. %s. attr=%s, contract_address=%s, token_id=%s",
                    e,
                    attr,
                    nft.token_address,
                    nft.token_id,
                )
                attributes = []

        result = models.NftMetadata(
            owner=nft_metadata.owner_of,
            chain=models.Chain.BINANCE.value,
            contract_address=nft.token_address,
            contract_name=nft_metadata.name,
            token_id=nft.token_id,
            token_type=nft_metadata.contract_type,
            name=name,
            description=str(token_data.get("description")),
            image=token_data.get("image"),
            animation_url=token_data.get("animation_url"),
            source_url=None,
            attributes=attributes,
            external_url=token_data.get("external_url"),
            token_data=token_data,
            cached=True,
        )
        self.repo.set_NFT_metadata(result)
        result.cached = False
        return result

    def _get_nft_metadata(self, nft: moralis.MoralisOwnedNft) -> models.NftMetadata:
        metadata = self.repo.get_NFT_metadata(
            models.Chain.BINANCE, nft.token_address, nft.token_id
        )
        if metadata:
            return metadata
        return self._get_nft_metadata_from_api(nft)

    def _parse_metadata(self, metadata: str) -> NFTTokenJson:
        data = json.loads(metadata)
        return data

    def _get_token_data(self, nft: moralis.MoralisNFTMetadata) -> NFTTokenJson:
        """metadata 에 data 있는 경우"""
        if nft.metadata is not None:
            return self._parse_metadata(nft.metadata)
        elif nft.token_uri is not None:
            log.debug("moralis nft metadata nft.metadata is None. %s", nft)
            return self._get_token_data_by_uri(nft.token_uri)
        else:
            log.warning("can't get token data from moralis nft metadata. nft=%s", nft)
            return {
                "name": "No name",
                "image": None,
                "attributes": [],
                "description": None,
            }


class NFTService:
    def __init__(
        self,
        ethereum: NFTServiceProtocol,
        polygon: NFTServiceProtocol,
        klaytn: NFTServiceProtocol,
        binance: NFTServiceProtocol,
        repo: repository.NFTSourceRepositoryProtocol,
    ):
        self.chain_map = {
            models.Chain.ETHEREUM: ethereum,
            models.Chain.POLYGON: polygon,
            models.Chain.KLAYTN: klaytn,
            models.Chain.BINANCE: binance,
        }
        self.repo = repo

    def get_NFTs_by_owner(
        self, chain: models.Chain, owner: str, cursor: str = None, resync: bool = False
    ) -> OwnedNftResult:
        nft_srv: NFTServiceProtocol = self.chain_map[chain]
        owned_nfts_result = nft_srv.get_NFTs_by_owner(owner, cursor, resync)
        return owned_nfts_result

    def get_NFT_by_contract_token_id(
        self, chain: models.Chain, contract_address: str, token_id: str, resync: bool
    ) -> Optional[models.NftMetadata]:
        nft_srv: NFTServiceProtocol = self.chain_map[chain]
        return nft_srv.get_NFT_by_contract_token_id(contract_address, token_id, resync)
