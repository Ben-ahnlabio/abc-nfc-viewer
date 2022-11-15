import os
import json
import pathlib
import tempfile
from typing import Optional
from anv import models
from anv import api
from anv.api import alchemy, kas, moralis, nft, infura
from anv.repository import NFTMetadataRespository, DiskRepository
from anv.api.ipfs import IPFSProxy

import web3
import pytest


@pytest.fixture
def fake_kas_credential_json():
    """fake kas credential json 을 생성하고
    'KAS_CREDENTIAL_JSON_PATH' 환경변수를 임시 변경
    fixture 종료 후 원상복구
    """
    with tempfile.TemporaryDirectory() as dir:
        fake_kas_credential = pathlib.Path(dir) / "kas-credential.json"
        with fake_kas_credential.open("w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "accessKeyId": "fake_access_key",
                        "secretAccessKey": "fake_secret_key",
                        "authorization": "fake_authorization",
                    }
                )
            )
        KAS_CREDENTIAL_JSON_PATH = os.getenv("KAS_CREDENTIAL_JSON_PATH")
        yield fake_kas_credential
        if KAS_CREDENTIAL_JSON_PATH is not None:
            os.environ["KAS_CREDENTIAL_JSON_PATH"] = KAS_CREDENTIAL_JSON_PATH


@pytest.fixture
def fake_kas_credential_env():
    os.environ["KAS_ACCESS_KEY_ID"] = "fake_access_key_id"
    os.environ["KAS_AUTHORIZATION"] = "fake_authorization"
    os.environ["KAS_SECRET_ACCESS_KEY"] = "fake_secret_key"
    yield


@pytest.fixture
def alchemy_api_key_env():
    os.environ["ALCHEMY_API_KEY"] = "O06KHzfPbklzwxDp8Z4KDrxIMmazK85c"
    os.environ["ALCHEMY_ETHER_MAIN_API_KEY"] = "O06KHzfPbklzwxDp8Z4KDrxIMmazK85c"
    os.environ["ALCHEMY_POLYGON_MAIN_API_KEY"] = "HCcxBsPAawcztXq5R7w3zRZb2VeX2ZGl"
    os.environ["ALCHEMY_SOLANA_MAIN_API_KEY"] = "EE1vFxSrdfHZClzRQo1tWg_IuyHqf7xu"


@pytest.fixture
def moralis_api_key_env():
    os.environ[
        "MORALIS_API_KEY"
    ] = "WR7xp7atOQ1XlFLywNisHfWUSLZT3EYnr13AiiLgVKOJCVlU1cxOFpqWrZorpSsF"


@pytest.fixture
def alchemy_api(alchemy_api_key_env):
    yield alchemy.AlchemyApi()


@pytest.fixture
def kas_env():
    os.environ["KAS_ACCESS_KEY_ID"] = "KASKOTSLZ89LS5RRCULWECVW"
    os.environ["KAS_SECRET_ACCESS_KEY"] = "__9FCFEi_IOdydovTLyMAO3Nt2XRIUf3m2pt9IZJ"
    os.environ[
        "KAS_AUTHORIZATION"
    ] = "Basic S0FTS09UU0xaODlMUzVSUkNVTFdFQ1ZXOl9fOUZDRkVpX0lPZHlkb3ZUTHlNQU8zTnQyWFJJVWYzbTJwdDlJWko="


@pytest.fixture
def kas_api(kas_env):
    yield kas.KasApi()


@pytest.fixture
def moralis_api(moralis_api_key_env):
    yield moralis.MorailsApi()


@pytest.fixture
def nft_api(alchemy_api):
    class Repo(NFTMetadataRespository):
        def get_NFT_metadata(
            self, network: models.Chain, contract_address: str, token_id: str
        ) -> Optional[models.NftMetadata]:
            return None

    yield nft.NftApi(Repo(), alchemy_api)


@pytest.fixture
def disk_repo():
    yield DiskRepository()


@pytest.fixture
def ethereum_api(disk_repo, ipfs, alchemy_api):
    yield api.EthereumApi(disk_repo, ipfs, alchemy_api)


@pytest.fixture
def klaytn_api(disk_repo, ipfs, kas_api):
    yield api.KlaytnApi(disk_repo, ipfs, kas_api)


@pytest.fixture
def infura_env():
    os.environ["INFURA_API_KEY"] = "c20947b695d14428968c560f69976d74"
    os.environ["INFURA_SECRET_KEY"] = "f44dc4afe25c4e298705a187977b5405"
    yield


@pytest.fixture
def infura_api(infura_env):
    yield infura.InfuraApi()


@pytest.fixture
def ipfs():
    yield IPFSProxy()


@pytest.fixture
def web3_obj():
    infura_url = "https://mainnet.infura.io/v3/c20947b695d14428968c560f69976d74"
    yield web3.Web3(web3.Web3.HTTPProvider(infura_url))
