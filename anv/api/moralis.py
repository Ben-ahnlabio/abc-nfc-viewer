import enum
import logging
import os
from typing import List, Literal, Optional

import pydantic
import requests

log = logging.getLogger(f"anv.{__name__}")

PAGE_SIZE = 20


class MoralisOwnedNft(pydantic.BaseModel):
    token_address: str
    token_id: str
    owner_of: Optional[str]
    block_number: Optional[str]
    block_number_minted: Optional[str]
    token_hash: Optional[str]
    amount: Optional[str]
    contract_type: Optional[str]
    name: Optional[str]
    symbol: Optional[str]
    token_uri: Optional[str]
    metadata: Optional[str]
    last_token_uri_sync: Optional[str]
    last_metadata_sync: Optional[str]
    minter_address: Optional[str]


class MoralisOwnedNftResult(pydantic.BaseModel):
    cursor: Optional[str]
    owned_nfts: List[MoralisOwnedNft]


class MoralisNFTMetadata(pydantic.BaseModel):
    token_address: str
    token_id: str
    owner_of: str
    block_number: str
    block_number_minted: str
    token_hash: str
    amount: str
    contract_type: str
    name: str
    symbol: str
    token_uri: Optional[str]  # None 인 경우 있음
    metadata: Optional[str]  # None 인 경우 있음
    # last_token_uri_sync: str
    # last_metadata_sync: str
    # minter_address: str
    # transfer_index: str

    def __str__(self):
        return f"[{self.name}] {self.token_address=} - {self.token_id=}"


class MorailsNetwork(enum.Enum):
    EthereumMainNet = "eth"
    BinanceMainNet = "bsc"
    BinanceTestNet = "0x61"


class MorailsApi:
    def __init__(self):
        self.api_key = os.getenv("MORALIS_API_KEY")

    def get_NFT_metadata(
        self, network: MorailsNetwork, contract_address: str, token_id: str
    ) -> MoralisNFTMetadata:
        log.debug(
            "getting moralis nft metadata contract_address=%s token_id=%s",
            contract_address,
            token_id,
        )
        metadata = self.get_NFT_metadata_raw(network, contract_address, token_id)
        return MoralisNFTMetadata.parse_obj(metadata)

    def get_NFTs(
        self, network: MorailsNetwork, owner: str, cursor: str = None
    ) -> MoralisOwnedNftResult:
        # TODO: 100 개의 NFT 만 가져온다. page 이동 필요
        owned_nfts = self.get_NFTs_raw(network, owner, cursor)
        return MoralisOwnedNftResult(
            cursor=owned_nfts["cursor"],
            owned_nfts=[MoralisOwnedNft.parse_obj(nft) for nft in owned_nfts["result"]],
        )

    def get_NFTs_raw(
        self, network: MorailsNetwork, owner: str, cursor: str = None
    ) -> dict:
        """
        https://docs.moralis.io/reference/getwalletnfts
        """

        headers = {"accept": "application/json", "X-API-Key": self.api_key}
        params = {
            "chain": network.value,
            "format": "decimal",
            "cursor": cursor,
            "limit": PAGE_SIZE,  # 20
        }

        url = f"https://deep-index.moralis.io/api/v2/{owner}/nft"
        return self._api_request("get", url, params=params, headers=headers)

    def get_NFT_metadata_raw(
        self, network: MorailsNetwork, contract_address: str, token_id: str
    ):
        """
        https://docs.moralis.io/reference/getnftmetadata
        """
        headers = {"accept": "application/json", "X-API-Key": self.api_key}
        params = {"chain": network.value}

        url = f"https://deep-index.moralis.io/api/v2/nft/{contract_address}/{token_id}"
        return self._api_request("get", url, params=params, headers=headers)

    def get_collection_metadata_raw(
        self, network: MorailsNetwork, contract_address: str
    ):
        """
        https://docs.moralis.io/reference/getnftcontractmetadata

        Response Example:

        >>> {
            "token_address": "0x2d30ca6f024dbc1307ac8a1a44ca27de6f797ec22ef20627a1307243b0ab7d09",
            "name": "KryptoKitties",
            "synced_at": "string",
            "symbol": "RARI",
            "contract_type": "ERC721"
        }
        """

        headers = {"accept": "application/json", "X-API-Key": self.api_key}
        params = {"chain": network.value}

        url = f"https://deep-index.moralis.io/api/v2/nft/{contract_address}/metadata"
        return self._api_request("get", url, params=params, headers=headers)

    def _api_request(
        self,
        method: Literal["get", "put", "post"],
        url: str,
        headers: dict,
        params: dict = None,
    ) -> dict:

        try:
            with requests.Session() as session:
                r = session.request(method, url, params=params, headers=headers)
                r.raise_for_status()
                return r.json()
        except requests.exceptions.HTTPError as e:
            log.warning(f"KAS API request failed: {e}")
            raise MoralisApiError(e)


class MoralisApiError(Exception):
    pass
