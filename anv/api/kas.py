import enum
import json
import logging
import os
import pathlib
from typing import Iterable, List, Literal, Optional, TypedDict

import pydantic
import requests

PAGE_SIZE = 20

log = logging.getLogger(f"anv.{__name__}")


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
    MT = "mt"


class KlaytnContract(pydantic.BaseModel):
    address: str
    name: str
    symbol: str


class KlaytnTransferHistory(pydantic.BaseModel):
    transfer_type: TokenKind
    contract: KlaytnContract
    from_address: str
    to_address: str
    token_id: str


class KlaytnOwnedNft(pydantic.BaseModel):
    contract_address: str
    token_id: str
    owner: Optional[str]
    previous_owner: Optional[str]
    token_uri: Optional[str]
    transaction_hash: Optional[str]
    updated_at: Optional[int]
    created_at: Optional[int]


class KlaytnOwndNftResult(pydantic.BaseModel):
    cursor: Optional[str]
    owned_nfts: List[KlaytnOwnedNft]


KlaytnNftResultTypeDef = TypedDict(
    "KlaytnNftResultTypeDef",
    {
        "tokenId": str,
        "owner": str,
        "previousOwner": str,
        "tokenUri": str,
        "transactionHash": str,
        "createdAt": int,
        "updatedAt": int,
    },
)


class KasApiError(Exception):
    pass


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

    def get_nft_contract_raw(self, chain_id: ChainId, nft_contract: str):
        """curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/nft/0x90d535c434e967ec6e9accb0de5dcb34010865e0" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}"""

        headers = {"x-chain-id": chain_id.value}
        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{nft_contract}"

        return self._kas_api_request("get", url, headers=headers)

    def get_nft_transfer_history_by_owner(
        self, chain_id: ChainId, owner: str
    ) -> List[KlaytnTransferHistory]:
        result = self.get_transfer_history_by_account_raw(
            chain_id, owner, (TokenKind.NFT,)
        )
        transfer_history = []
        for item in result["items"]:
            contract = item["contract"]
            history = KlaytnTransferHistory(
                transfer_type=TokenKind(item["transferType"]),
                contract=KlaytnContract(
                    address=contract["address"],
                    name=contract["name"],
                    symbol=contract["symbol"],
                ),
                token_id=item["tokenId"],
                from_address=item["from"],
                to_address=item["to"],
            )
            transfer_history.append(history)
        return transfer_history

    def get_transfer_history_by_account_raw(
        self, chain_id: ChainId, owner: str, kind: Iterable[TokenKind]
    ):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token-history

        ?????? EOA??? ????????? ?????? ?????? ????????? ???????????????.

        curl --location --request GET "https://th-api.klaytnapi.com/v2/transfer/account/0xc060632ad88d0dec2bbc44bbea9d4c48c2ead48f?kind=klay,ft,nft&range=1592360291,15991809920" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}
        """

        headers = {"x-chain-id": chain_id.value}
        params = {"kind": ",".join([token.value for token in kind])}
        url = f"https://th-api.klaytnapi.com/v2/transfer/account/{owner}"

        return self._kas_api_request("get", url, headers=headers, params=params)

    def get_nft_list_by_owner(
        self, chain_id: ChainId, owner: str, contract_address: str
    ) -> List[KlaytnOwnedNft]:
        result = self.get_nft_list_by_owner_raw(chain_id, owner, contract_address)
        return [
            KlaytnOwnedNft(
                contract_address=contract_address,
                token_id=item["tokenId"],
                owner=item["owner"],
                previous_owner=item["previousOwner"],
                token_uri=item["tokenUri"],
                transaction_hash=item["transactionHash"],
                created_at=item["createdAt"],
                updated_at=item["updatedAt"],
            )
            for item in result["items"]
        ]

    def get_nft_list_by_owner_raw(
        self, chain_id: ChainId, owner: str, contract_address: str
    ):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token

        ?????? EOA??? ?????? NFT ????????? ???????????????. ??? ????????? ???????????? ?????? ?????????????????? ????????? ???????????? ?????????.        

        curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/nft/0x251f622e8b5e713f357e9c4d990e91da2f448134/owner/0xe5389503156ee02775ee18552f0c9d9846b66a91size=100&cursor=J9Ag...VM6z" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}
        """
        headers = {"x-chain-id": chain_id.value}
        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{contract_address}/owner/{owner}"

        return self._kas_api_request("get", url, headers=headers)

    def get_ft(self, chain_id: ChainId, contract_address: str):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-contract#ft-1

        ?????? FT ???????????? ????????? ???????????????.
        FT ??????????????? Klaytn??? ???????????? ????????? ??????????????? ???????????????.
        ??? ??????????????? ?????? ?????? ??????(Fungible Token, FT)??? ??????, ??????, ???????????? ????????? ???????????????.

        curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/ft/0xbe7377db700664331beb28023cfbd46de079efac" \
        --header "x-chain-id: {chain-id}" \
        -u {access-key-id}:{secret-access-key}
        
        """

        headers = {"x-chain-id": chain_id.value}
        url = f"https://th-api.klaytnapi.com/v2/contract/ft/{contract_address}"

        return self._kas_api_request("get", url, headers=headers)

    def get_nft(
        self, chain_id: ChainId, nft_contract: str, token_id: str
    ) -> KlaytnNftResultTypeDef:
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token
        https://refs.klaytnapi.com/ko/tokenhistory/latest#operation/getNftById

        ?????? NFT ????????? ???????????????.

        NFT ??????????????? Klaytn??? ???????????? ????????? ??????????????? ???????????????. ??? ??????????????? ?????? ?????? ??????(Non-Fungible Token, NFT)??? ??????, ??????, ???????????? ????????? ???????????????.

        Return:
        ?????? ?????????
        >>> {
            "tokenId": "0x2",
            "owner": "0xe5389503156ee02775ee18552f0c9d9846b66a91",
            "previousOwner": "0x0000000000000000000000000000000000000000",
            "tokenUri": "http://172.16.15.49:8080/meta/item2",
            "transactionHash": "0xc7d07066e4e42a7d896c34420ed43568ba44ae15a8ef771b13ba1f6f2\\ d2820c4",
            "createdAt": 1597304701,
            "updatedAt": 1597304701
        }
        """

        headers = {"x-chain-id": chain_id.value}
        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{nft_contract}/token/{token_id}"

        return self._kas_api_request("get", url, headers=headers)

    def get_nft_list(
        self,
        chain_id: ChainId,
        nft_contract: str,
        size: int = None,
        cursor: str = None,
    ):
        """
        https://docs.klaytnapi.com/tutorial/token-history-api/th-api-token

        ???????????? ?????? NFT ?????????????????? ????????? NFT ????????? ???????????????.

        `curl --location --request GET "https://th-api.klaytnapi.com/v2/contract/nft/0x90d535c434e967ec6e9accb0de5dcb34010865e0/token?size=100&cursor=J9Ag...VM6z" \
            --header "x-chain-id: {chain-id}" \
            -u {access-key-id}:{secret-access-key}`

        Args:
            chain_id: Cypress(?????????), Baobab(????????????)
            nfs_contract: ??????????????? NFT ??????????????? ??????
            size: ?????? ????????? ?????? (min=1, max=1000, default=100)
            cursor: ???????????????????????? ?????? ????????? ?????? ??? ????????? ??????
        """
        headers = {"x-chain-id": chain_id.value}
        params = {"size": size, "cursor": cursor}

        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{nft_contract}/token"
        return self._kas_api_request("get", url, headers=headers, params=params)

    def get_contracts_by_owner(
        self, chain_id: ChainId, owner: str, kind: Iterable[TokenKind]
    ):
        """EOA??? ???????????? ?????? EOA??? ????????? ???????????? ???????????? ????????? ???????????????.

        https://refs.klaytnapi.com/ko/tokenhistory/latest#operation/getListOfContractByOwnerAddress

        """

        headers = {"x-chain-id": chain_id.value}

        # https://th-api.klaytnapi.com/v2/account/{address}/contract
        url = f"https://th-api.klaytnapi.com/v2/account/{owner}/contract"
        return self._kas_api_request("get", url, headers=headers)

    def get_tokens_by_owner(
        self,
        chain_id: ChainId,
        owner: str,
        kind: Iterable[TokenKind],
        cursor: str = None,
    ) -> KlaytnOwndNftResult:
        """EOA??? ???????????? ?????? EOA??? ????????? ?????? ????????? ???????????????.

        https://refs.klaytnapi.com/ko/tokenhistory/latest#operation/getListOfTokenByOwnerAddress

        """
        result = self.get_tokens_by_owner_raw(chain_id, owner, kind, cursor)
        return KlaytnOwndNftResult(
            cursor=result["cursor"],
            owned_nfts=[
                KlaytnOwnedNft(
                    contract_address=item["contractAddress"],
                    token_id=item["extras"]["tokenId"],
                    owner=owner,
                    previous_owner=item["lastTransfer"]["transferFrom"],
                    token_uri=item["extras"]["tokenUri"],
                    transaction_hash=item["lastTransfer"]["transactionHash"],
                    updated_at=item["updatedAt"],
                    created_at=None,  # ????????????
                )
                for item in result["items"]
            ],
        )

    def get_tokens_by_owner_raw(
        self,
        chain_id: ChainId,
        owner: str,
        kind: Iterable[TokenKind],
        cursor: str = None,
    ):
        """EOA??? ???????????? ?????? EOA??? ????????? ?????? ????????? ???????????????.

        https://refs.klaytnapi.com/ko/tokenhistory/latest#operation/getListOfTokenByOwnerAddress

        returns: dict,
        ?????? ??????
        >>> {
            "items": [
                {
                    "kind": "nft",
                    "contractAddress": "0x77777777777b7fdaa2fceb47ebde85cd461f8859",
                    "updatedAt": 1664652860,
                    "balance": "0x1",
                    "lastTransfer": {
                        "transactionHash": "0xd02b82e50bce86ad883fd3efc92869f7ee8148ed9accb11ec29f658b3a816aa2",
                        "transferFrom": "0x0000000000000000000000000000000000000000",
                        "transferTo": "0xfe463e0d253ea6972f13ea93516da762503d0d2a"
                    },
                    "extras": {
                        "tokenId": "0xd89",
                        "tokenUri": "https://7nftbits.com/json/3465.json"
                    }
                }
            ]
        }


        """

        headers = {"x-chain-id": chain_id.value}
        params = {
            "kind": ",".join([token.value for token in kind]),
            "cursor": cursor,
            "size": PAGE_SIZE,
        }

        # https://th-api.klaytnapi.com/v2/account/{address}/token
        url = f"https://th-api.klaytnapi.com/v2/account/{owner}/token"
        return self._kas_api_request("get", url, params=params, headers=headers)

    def update_nft_contract_metadata(self, chain_id: ChainId, contract_address: str):
        """
        ?????? NFT ??????????????? ??????????????? ?????? ????????????

        NFT ???????????? ???????????????(name, symbol) ????????? ??????????????? ????????? ?????? ????????? ???????????? ?????????

        PUT https://th-api.klaytnapi.com/v2/contract/nft/{nft-address}/metadata
        """

        headers = {"x-chain-id": chain_id.value}

        # https://th-api.klaytnapi.com/v2/account/{address}/token
        url = (
            f"https://th-api.klaytnapi.com/v2/contract/nft/{contract_address}/metadata"
        )
        return self._kas_api_request("put", url, headers=headers)

    def update_nft_token_metadata(
        self, chain_id: ChainId, contract_address: str, token_id: str
    ):
        """
        PUT https://th-api.klaytnapi.com/v2/contract/nft/{nft-address}/token/{token-id}/metadata
        """

        headers = {"x-chain-id": chain_id.value}

        # https://th-api.klaytnapi.com/v2/account/{address}/token
        url = f"https://th-api.klaytnapi.com/v2/contract/nft/{contract_address}/token/{token_id}/metadata"
        return self._kas_api_request("put", url, headers)

    def _kas_api_request(
        self,
        method: Literal["get", "put", "post"],
        url: str,
        headers: dict,
        params: dict = None,
    ) -> dict:

        try:
            with requests.Session() as session:
                session.auth = (self.access_key_id, self.secret_access_key)
                r = session.request(method, url, params=params, headers=headers)
                r.raise_for_status()
                return r.json()
        except requests.exceptions.HTTPError as e:
            log.warning(f"KAS API request failed: {e}")
            raise KasApiError(e)
