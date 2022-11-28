import logging
import os
import enum
from typing import List, Optional
import pydantic
import requests
from anv.models import Chain, NftMetadata, NftAttribute

log = logging.getLogger(f"anv.{__name__}")

# https://solana-mainnet.g.alchemy.com/v2/EE1vFxSrdfHZClzRQo1tWg_IuyHqf7xu
# https://arb-mainnet.g.alchemy.com/v2/eIgDnqhsy6gAL8Z7wYalt3Te3wBn-Vlz
# https://polygon-mainnet.g.alchemy.com/v2/HCcxBsPAawcztXq5R7w3zRZb2VeX2ZGl

PAGE_SIZE = 20


class AlchemyNet(enum.Enum):
    EthMainNet = "eth-mainnet"
    PolygonMainNet = "polygon-mainnet"
    SolanaMainNet = "solana-mainnet"


class AlchemyOwnedNft(pydantic.BaseModel):
    contract_address: str
    token_id: str
    balance: Optional[int]


class AlchemyOwnedNftResult(pydantic.BaseModel):
    cursor: Optional[str]
    owned_nfts: List[AlchemyOwnedNft]


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

    def get_NFTs(
        self, network: AlchemyNet, owner: str, cursor: str = None
    ) -> AlchemyOwnedNftResult:
        result = self.get_NFTs_raw(network, owner, cursor)
        return AlchemyOwnedNftResult(
            cursor=result.get("pageKey"),
            owned_nfts=[
                AlchemyOwnedNft(
                    contract_address=nft["contract"]["address"],
                    token_id=nft["id"]["tokenId"],
                    balance=nft["balance"],
                )
                for nft in result["ownedNfts"]
            ],
        )

    def get_NFTs_raw(self, network: AlchemyNet, owner: str, cursor: str = None):
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
            ],
            "pageKey": "..."
        }
        """

        headers = {"accept": "application/json"}
        params = {
            "owner": owner,
            "withMetadata": "false",
            "pageKey": cursor,
            "pageSize": PAGE_SIZE,
        }
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
        contract_name = result.get("contractMetadata", {}).get("name", "")
        if not name:
            log.warning(
                "nft name is not exist. contract_address=%s, token_id=%s",
                contract_address,
                token_id,
            )
            # metadata 에 name 이 없는 경우는 contract_name #{token_id} 형식으로 출력한다.
            if contract_name:
                name = contract_name
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

        attributes = []
        for attr in metadata.get("attributes", []):
            try:
                attributes.append(
                    NftAttribute(
                        trait_type=attr["trait_type"],
                        value=attr["value"],
                        display_type=attr.get("display_type"),
                    )
                )
            except KeyError as e:
                log.warning(
                    "NftMetadata attribute error. %s. contract_address=%s, token_id=%s",
                    e,
                    contract_address,
                    token_id,
                )
                attributes = []

        if network == network.EthMainNet:
            chain = Chain.ETHEREUM.value
        elif network == network.PolygonMainNet:
            chain = Chain.POLYGON.value

        return NftMetadata(
            chain=chain,
            contract_address=contract_address,
            contract_name=contract_name,
            token_id=token_id,
            token_type=token_type,
            name=name,
            description=metadata.get("description"),
            image=metadata.get("image"),
            animation_url=metadata.get("animation_url"),
            attributes=attributes,
            external_url=metadata.get("external_url"),
            token_data=metadata,
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

        return 값은 아래 dict 와 같은 형태
        >>> {
            "contract": { "address": "0x2931b181ae9dc8f8109ec41c42480933f411ef94" },
            "id": {
                "tokenId": "0x0000000000000000000000000000000000000000000000000000000000000262",
                "tokenMetadata": { "tokenType": "ERC721" }
            },
            "title": "SlimHood #610",
            "description": "They all wear hoods, but each SlimHood is unique.",
            "tokenUri": {
                "raw": "ipfs://QmSuV1wfkV2MrkR52KcbYM2717j5L1EPqLknZKY1cLKxMB/610",
                "gateway": "https://alchemy.mypinata.cloud/ipfs/QmSuV1wfkV2MrkR52KcbYM2717j5L1EPqLknZKY1cLKxMB/610"
            },
            "media": [
                {
                "raw": "ipfs://QmPCzRHRgCdPrhNnfG9tPvM5jp18TmoJwBrfkgcyFipe7b/610.gif",
                "gateway": "https://ipfs.io/ipfs/QmPCzRHRgCdPrhNnfG9tPvM5jp18TmoJwBrfkgcyFipe7b/610.gif"
                }
            ],
            "metadata": {
                "name": "SlimHood #610",
                "description": "They all wear hoods, but each SlimHood is unique.",
                "image": "ipfs://QmPCzRHRgCdPrhNnfG9tPvM5jp18TmoJwBrfkgcyFipe7b/610.gif",
                "attributes": [
                { "value": "Orange/Red/White/Green", "trait_type": "Hoodie" },
                ]
            },
            "timeLastUpdated": "2022-11-04T00:20:33.154Z",
            "contractMetadata": {
                "name": "SlimHoods",
                "symbol": "SLMHDS",
                "totalSupply": "5000",
                "tokenType": "ERC721",
                "openSea": {
                "floorPrice": 0.0678,
                "collectionName": "SlimHoods",
                "safelistRequestStatus": "verified",
                "imageUrl": "https://i.seadn.io/gae/_PXs9iFB8iSm40EfmsjJ_6VHZ7eescWHfZ_PVhinl8AFj26BjTh38iDW1Sr3bR3MU8wsTFD8tbXtaFVZPMRa9XNH-sucajGHNB2gkw?w=500&auto=format",
                "description": "SlimHoods are a collection of 5000 randomly generated NFTs on the Ethereum blockchain.\r\n\r\nThey all wear hoods, but each SlimHood is unique.\r\n\r\nSlimHoods is the first collection by Random Character Collective.",
                "externalUrl": "http://slimhoods.com",
                "twitterUsername": "SlimHoods",
                "discordUrl": "https://discord.gg/rndm",
                "lastIngestedAt": "2022-11-01T05:57:33.000Z"
                }
            }
            }

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

    def get_contracts_for_owner(
        self, network: AlchemyNet, owner: str, cursor: str = None
    ):
        """
        https://docs.alchemy.com/reference/getcontractsforowner

        Args:
            owner: owner address
        """

        headers = {"accept": "application/json"}
        params = {
            "owner": owner,
            "pageKey": cursor,
            "pageSize": PAGE_SIZE,
        }
        url = f"https://{network.value}.g.alchemy.com/nft/v2/{self.api_key[network]}/getContractsForOwner"

        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
