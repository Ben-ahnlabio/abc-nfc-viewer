import os
import enum

import requests

# https://solana-mainnet.g.alchemy.com/v2/EE1vFxSrdfHZClzRQo1tWg_IuyHqf7xu
# https://arb-mainnet.g.alchemy.com/v2/eIgDnqhsy6gAL8Z7wYalt3Te3wBn-Vlz
# https://polygon-mainnet.g.alchemy.com/v2/HCcxBsPAawcztXq5R7w3zRZb2VeX2ZGl


class AlchemyNetwork(enum.Enum):
    EthereumMainNet = "eth-mainnet"
    PolygonMainNet = "polygon-mainnet"


class AlchemyApi:
    def __init__(self):
        self.api_key = os.getenv("ALCHEMY_API_KEY")
        self.ether_main_api_key = os.getenv("ALCHEMY_API_KEY")
        self.ether_main_api_key = os.getenv("ALCHEMY_API_KEY")

    def get_NFTs(self, network: AlchemyNetwork, owner: str):
        """
        https://docs.alchemy.com/reference/getnfts

        Args:
            owner: 소유자 지갑주소
        """

        headers = {"accept": "application/json"}
        params = {"owner": owner, "withMetadata": "false"}
        url = f"https://{network.value}.g.alchemy.com/nft/v2/{self.api_key}/getNFTs"
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_NFT_metadata(
        self, network: AlchemyNetwork, contract_address: str, token_id: str
    ):
        """
        https://docs.alchemy.com/reference/getnftmetadata

        Args:
            contract_address: contract address
            token_id: token: token id
        """

        headers = {"accept": "application/json"}
        params = {"contractAddress": contract_address, "tokenId": token_id}
        url = f"https://{network.value}.g.alchemy.com/nft/v2/{self.api_key}/getNFTMetadata"
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
