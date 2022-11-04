import enum
import json
import os
import pathlib
from typing import TypedDict, Iterable

import requests


class KasCredentialJson(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    authorization: str


class ChainId(enum.Enum):
    Cypress = "8217"
    Baobab = "1001"


class TokenKind(enum.Enum):
    KLAY = "klay"
    FT = "ft"
    NFT = "nft"


class KasApi:
    def __init__(self):
        kas_credential_path = os.getenv("KAS_CREDENTIAL_JSON_PATH")
        if kas_credential_path:
            self.credential_path = pathlib.Path(kas_credential_path)
            with self.credential_path.open("r", encoding="utf-8") as f:
                credential: KasCredentialJson = json.loads(f.read())
                self.access_key_id = credential["accessKeyId"]
                self.secret_access_key = credential["secretAccessKey"]
                self.authorization = credential["authorization"]
        else:
            self.access_key_id = os.getenv("KAS_ACCESS_KEY_ID")
            self.authorization = os.getenv("KAS_AUTHORIZATION")
            self.secret_access_key = os.getenv("KAS_SECRET_ACCESS_KEY")

    def get_nft_contract(
        self,
        chain_id: ChainId,
        nft_contract: str,
    ):
        """curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/nft/0x90d535c434e967ec6e9accb0de5dcb34010865e0" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}"""
        headers = {"x-chain-id": chain_id.value}
        session = requests.Session()
        session.auth = (self.access_key_id, self.secret_access_key)
        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{nft_contract}"
        r = session.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_transfer_history_by_account(
        self, chain_id: ChainId, owner: str, kind: Iterable[TokenKind]
    ):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token-history

        특정 EOA가 토큰을 주고 받은 기록을 조회합니다.

        curl --location --request GET "https://th-api.klaytnapi.com/v2/transfer/account/0xc060632ad88d0dec2bbc44bbea9d4c48c2ead48f?kind=klay,ft,nft&range=1592360291,15991809920" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}
        """

        headers = {"x-chain-id": chain_id.value}
        params = {"kind": ",".join([token.value for token in kind])}
        session = requests.Session()
        session.auth = (self.access_key_id, self.secret_access_key)
        url = f"https://th-api.klaytnapi.com/v2/transfer/account/{owner}"
        r = session.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_nft_list_by_owner(
        self, chain_id: ChainId, owner: str, contract_address: str
    ):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token

        특정 EOA가 가진 NFT 목록을 조회합니다. 이 토큰은 라벨링된 토큰 컨트랙트에서 발행한 것이어야 합니다.        

        curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/nft/0x251f622e8b5e713f357e9c4d990e91da2f448134/owner/0xe5389503156ee02775ee18552f0c9d9846b66a91size=100&cursor=J9Ag...VM6z" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}
        """
        headers = {"x-chain-id": chain_id.value}
        session = requests.Session()
        session.auth = (self.access_key_id, self.secret_access_key)
        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{contract_address}/owner/{owner}"
        r = session.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_nft_info(
        self,
        chain_id: ChainId,
        nfs_contract: str,
        size: int = None,
        cursor: str = None,
    ):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token

        라벨링된 특정 NFT 컨트랙트에서 발행한 NFT 목록을 조회합니다.

        `curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/nft/0x90d535c434e967ec6e9accb0de5dcb34010865e0/token?size=100&cursor=J9Ag...VM6z" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}`

        Args:
            chain_id: Cypress(메인넷), Baobab(테스트넷)
            nfs_contract: 조회하려는 NFT 컨트랙트의 주소
            size: 응답 아이템 개수 (min=1, max=1000, default=100)
            cursor: 페이지네이션으로 다음 요청을 보낼 때 필요한 커서
        """
        headers = {"x-chain-id": chain_id.value}
        params = {"size": size, "cursor": cursor}
        session = requests.Session()
        session.auth = (self.access_key_id, self.secret_access_key)

        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{nfs_contract}/token"
        r = session.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
