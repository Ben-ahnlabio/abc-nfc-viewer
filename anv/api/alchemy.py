import dataclasses
import logging
import os
import enum
from typing import List
import requests
from anv.models import Network, NftMetadata, NftAttribute

log = logging.getLogger(f"anv.{__name__}")

# https://solana-mainnet.g.alchemy.com/v2/EE1vFxSrdfHZClzRQo1tWg_IuyHqf7xu
# https://arb-mainnet.g.alchemy.com/v2/eIgDnqhsy6gAL8Z7wYalt3Te3wBn-Vlz
# https://polygon-mainnet.g.alchemy.com/v2/HCcxBsPAawcztXq5R7w3zRZb2VeX2ZGl


class AlchemyNet(enum.Enum):
    EthMainNet = "eth-mainnet"
    PolygonMainNet = "polygon-mainnet"
    SolanaMainNet = "solana-mainnet"


@dataclasses.dataclass
class AlchemyOwnedNft:
    contract_address: str
    token_id: str
    balance: int


class AlchemyApi:
    def __init__(self):
        self.ether_main_api_key = os.getenv("ALCHEMY_ETHER_MAIN_API_KEY")
        self.ploygon_main_api_key = os.getenv("ALCHEMY_POLYGON_MAIN_API_KEY")
        self.solana_main_api_key = os.getenv("ALCHEMY_SOLANA_MAIN_API_KEY")
        self.api_key = {
            AlchemyNet.EthMainNet: self.ether_main_api_key,
            AlchemyNet.PolygonMainNet: self.ploygon_main_api_key,
            AlchemyNet.SolanaMainNet: self.solana_main_api_key,
        }

    def get_NFTs(self, network: AlchemyNet, owner: str) -> List[AlchemyOwnedNft]:
        result = self.get_NFTs_raw(network, owner)
        return [
            AlchemyOwnedNft(
                contract_address=nft["contract"]["address"],
                token_id=nft["id"]["tokenId"],
                balance=nft["balance"],
            )
            for nft in result["ownedNfts"]
        ]

    def get_NFTs_raw(self, network: AlchemyNet, owner: str):
        """
        https://docs.alchemy.com/reference/getnfts

        Args:
            owner: 소유자 지갑주소

        Examples:
        >>> {
            "ownedNfts": [
                {
                    "contract": { "address": "0x039b52db88ae51b86b7ab091fa710082ef60dd7b" },
                    "id": {
                        "tokenId": "0x0000000000000000000000000000000000000000000000000000000000000016"
                    },
                    "balance": "1"
                },
            ]
        }
        """

        headers = {"accept": "application/json"}
        params = {"owner": owner, "withMetadata": "false"}
        url = f"https://{network.value}.g.alchemy.com/nft/v2/{self.api_key[network]}/getNFTs"
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_NFT_metadata(
        self, network: AlchemyNet, contract_address: str, token_id: str
    ) -> NftMetadata:
        result = self.get_NFT_metadata_raw(network, contract_address, token_id)
        metadata = result["metadata"]
        name = metadata.get("name")
        if not name:
            log.warning(
                "nft name is not exist. contract_address=%s, token_id=%s",
                contract_address,
                token_id,
            )
            # metadata 에 name 이 없는 경우는 contract name 을 대신한다.
            contract_name = result.get("contractMetadata", {}).get("name", "")
            if contract_name:
                name = f"[Contract] {contract_name}"
            else:
                name = ""

        try:
            token_type = result["id"]["tokenMetadata"]["tokenType"]
        except KeyError as e:
            log.warning(
                "token_type is not exist. %s contract_address=%s, token_id=%s",
                e,
                contract_address,
                token_id,
            )
            token_type = ""

        return NftMetadata(
            network=Network.ETHEREUM.value,
            contract_address=contract_address,
            token_id=token_id,
            token_type=token_type,
            name=name,
            description=metadata.get("description"),
            image=metadata.get("image"),
            attributes=[
                NftAttribute(trait_type=attr["trait_type"], value=attr["value"])
                for attr in metadata.get("attributes", [])
            ],
            cached=False,
        )

    def get_NFT_metadata_raw(
        self, network: AlchemyNet, contract_address: str, token_id: str
    ):
        """
        https://docs.alchemy.com/reference/getnftmetadata

        Args:
            contract_address: contract address
            token_id: token: token id
        """

        headers = {"accept": "application/json"}
        params = {"contractAddress": contract_address, "tokenId": token_id}
        url = f"https://{network.value}.g.alchemy.com/nft/v2/{self.api_key[network]}/getNFTMetadata"
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_contract_metadata(self, network: AlchemyNet, contract_address: str):
        """
        https://docs.alchemy.com/reference/getcontractmetadata

        Args:
            contract_address: contract address
        """

        headers = {"accept": "application/json"}
        params = {"contractAddress": contract_address}
        url = f"https://{network.value}.g.alchemy.com/nft/v2/{self.api_key[network]}/getContractMetadata"

        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
