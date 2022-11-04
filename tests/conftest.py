import os
import json
import pathlib
import tempfile
from anv.api import alchemy, kas

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
