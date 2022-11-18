import logging
import os
import enum
from urllib.parse import urljoin
import requests

log = logging.getLogger(f"anv.{__name__}")


class ChainId(enum.Enum):
    EthereumMain = "1"
    EthereumGoerli = "5"
    PolygonMain = "137"
    PolygonMumbai = "80001"


class InfuraApi:
    def __init__(self):
        self.access_key_id = os.getenv("INFURA_API_KEY")
        self.secret_access_key = os.getenv("INFURA_SECRET_KEY")
        self.base_url = "https://mainnet.infura.io/"

    def get_NFTs(self, chain_id: ChainId, token_address: str):
        """
        https://docs.api.infura.io/nft/

        curl -X 'GET' \
        'https://nft.api.infura.io/networks/1/nfts/0xa9cb55d05d3351dcd02dd5dc4614e764ce3e1d6e' \
        -H 'accept: application/json' \
        -H 'Authorization: Basic YzIwOTQ3YjY5NWQxNDQyODk2OGM1NjBmNjk5NzZkNzQ6ZjQ0ZGM0YWZlMjVjNGUyOTg3MDVhMTg3OTc3YjU0MDU='
        
        """
        headers = {"accept": "application/json"}
        session = requests.Session()
        session.auth = (self.access_key_id, self.secret_access_key)
        url = urljoin(self.base_url, f"networks/{chain_id.value}/nfts/{token_address}")

        r = session.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_NFTs_by_owner(self, chain_id: ChainId, owner: str):
        """
        curl -X 'GET' \
        'https://nft.api.infura.io/networks/1/accounts/0x0a267cf51ef038fc00e71801f5a524aec06e4f07/assets/nfts' \
        -H 'accept: application/json' \
        -H 'Authorization: Basic cmljZXBvdGF0bzQwQGdtYWlsLmNvbTpxa3Foc2hhZGs0MA=='
        """
        headers = {"accept": "application/json"}
        session = requests.Session()
        session.auth = (self.access_key_id, self.secret_access_key)
        # url = urljoin(
        #     self.base_url, f"networks/{chain_id.value}/accounts/{owner}/assets/nfts"
        # )
        url = urljoin(self.base_url, f"accounts/{owner}/assets/nfts")
        # const apiUrl = `${this.#apiPath}/accounts/${publicAddress}/assets/nfts`;
        r = session.get(url, headers=headers)
        r.raise_for_status()
        return r.json()
