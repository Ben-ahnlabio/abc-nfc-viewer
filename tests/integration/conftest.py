import json
import os
import pathlib
import tempfile
from typing import Optional

import dotenv
import pytest
import web3

from anv import models, service, aws_s3
from anv.api import alchemy, infura, kas, moralis, nft
from anv.api.ipfs import IPFSProxy
from anv.repository import DiskRepository, NFTMetadataRespository, AWSS3SourceRepository


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
def env_from_file():
    yield dotenv.load_dotenv("anv/.env")


@pytest.fixture
def alchemy_api(env_from_file):
    yield alchemy.AlchemyApi()


@pytest.fixture
def kas_api(env_from_file):
    yield kas.KasApi()


@pytest.fixture
def moralis_api(env_from_file):
    yield moralis.MorailsApi()


@pytest.fixture
def nft_api(env_from_file):
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
def infura_api(env_from_file):
    yield infura.InfuraApi()


@pytest.fixture
def ipfs():
    yield IPFSProxy()


@pytest.fixture
def web3_obj():
    infura_api_key = os.getenv("INFURA_API_KEY")
    infura_url = f"https://mainnet.infura.io/v3/{infura_api_key}"
    yield web3.Web3(web3.Web3.HTTPProvider(infura_url))


@pytest.fixture
def binance_nft_service(disk_repo, ipfs, moralis_api):
    yield service.BinanceNFTService(disk_repo, ipfs, moralis_api)


@pytest.fixture
def binance_test_nft_service(disk_repo, ipfs, moralis_api):
    yield service.BinanceTestNFTService(disk_repo, ipfs, moralis_api)


@pytest.fixture
def ethereum_nft_service(disk_repo, ipfs, alchemy_api):
    yield service.EthereumNFTService(disk_repo, ipfs, alchemy_api)


@pytest.fixture
def polygon_nft_service(disk_repo, ipfs, alchemy_api):
    yield service.PolygonNFTService(disk_repo, ipfs, alchemy_api)


@pytest.fixture
def klaytn_nft_service(disk_repo, ipfs, kas_api):
    yield service.KlaytnNFTService(disk_repo, ipfs, kas_api)


@pytest.fixture
def klaytn_baobob_nft_service(disk_repo, ipfs, kas_api):
    yield service.KlaytnBaobobNFTService(disk_repo, ipfs, kas_api)


@pytest.fixture
def aws_s3_obj(env_from_file):
    yield aws_s3.AWSS3Storage()


@pytest.fixture
def s3_src_repo(aws_s3_obj, disk_repo, ipfs):
    yield AWSS3SourceRepository(aws_s3_obj, disk_repo, ipfs)
