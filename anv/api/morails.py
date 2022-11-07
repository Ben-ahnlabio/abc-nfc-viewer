import enum
import os

import requests


class MorailsNetwork(enum.Enum):
    EthereumMainNet = "eth"
    BinanceMainNet = "bsc"


class MorailsApi:
    def __init__(self):
        self.api_key = os.getenv("MORALIS_API_KEY")

    def get_NFT_metadata(
        self, network: MorailsNetwork, contract_address: str, token_id: str
    ):
        """
        https://docs.moralis.io/reference/getnftmetadata
        """
        headers = {"accept": "application/json", "X-API-Key": self.api_key}
        params = {"chain": network.value}

        url = f"https://deep-index.moralis.io/api/v2/nft/{contract_address}/{token_id}"
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()

        return r.json()

    def get_NFTs(self, network: MorailsNetwork, owner: str):
        """
        https://docs.moralis.io/reference/getwalletnfts
        """

        headers = {"accept": "application/json", "X-API-Key": self.api_key}
        params = {"chain": network.value, "format": "decimal"}

        url = f"https://deep-index.moralis.io/api/v2/{owner}/nft"
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()

        return r.json()
