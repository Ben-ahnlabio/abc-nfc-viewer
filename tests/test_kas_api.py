import json
from anv.api import kas


def test_create_kas_api_object(fake_kas_credential_json):
    kas_api = kas.KasApi()
    assert kas_api


def test_create_kas_api_object_with_env(fake_kas_credential_env):
    kas_api = kas.KasApi()
    assert kas_api


def test_get_nft_contract(kas_api: kas.KasApi):

    # ethan nft
    nft_contract = "0x590744cb8cf1a698d7db509b52bf209e3cccb8e0"
    result = kas_api.get_nft_contract(kas.ChainId.Cypress, nft_contract)
    assert result
    with open("kas_nft_contract_result.json", "w") as f:
        f.write(json.dumps(result))


def test_get_nft_by_owner(kas_api: kas.KasApi):
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"
    contract_address = "0x590744cb8cf1a698d7db509b52bf209e3cccb8e0"
    result = kas_api.get_nft_list_by_owner(kas.ChainId.Cypress, owner, contract_address)
    assert result
    with open("kas_nft_list_by_owner.json", "w") as f:
        f.write(json.dumps(result))


def test_get_transfer_history_by_owner(kas_api: kas.KasApi):
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"
    result = kas_api.get_transfer_history_by_account(
        kas.ChainId.Cypress, owner, (kas.TokenKind.NFT,)
    )
    assert result
    with open("get_transfer_history_by_account.json", "w") as f:
        f.write(json.dumps(result))
