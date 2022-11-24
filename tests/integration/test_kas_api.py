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
    result = kas_api.get_nft_contract_raw(kas.ChainId.Cypress, nft_contract)
    assert result
    with open("kas_nft_contract_result.json", "w") as f:
        f.write(json.dumps(result))


def test_get_nft_by_owner(kas_api: kas.KasApi):
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"
    contract_address = "0x590744cb8cf1a698d7db509b52bf209e3cccb8e0"
    result = kas_api.get_nft_list_by_owner_raw(
        kas.ChainId.Cypress, owner, contract_address
    )
    assert result
    with open("kas_nft_list_by_owner.json", "w") as f:
        f.write(json.dumps(result))


def test_get_transfer_history_by_owner(kas_api: kas.KasApi):
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"
    result = kas_api.get_transfer_history_by_account_raw(
        kas.ChainId.Cypress, owner, (kas.TokenKind.NFT,)
    )
    assert result
    with open("get_transfer_history_by_account.json", "w") as f:
        f.write(json.dumps(result))


def test_get_nft_list(kas_api: kas.KasApi):
    contract_address = "0x590744cb8cf1a698d7db509b52bf209e3cccb8e0"
    result = kas_api.get_nft_list(kas.ChainId.Cypress, contract_address)
    assert result
    with open("kas_nft_list_by_contract_addr.json", "w") as f:
        f.write(json.dumps(result))


def test_get_nft_contract(kas_api: kas.KasApi):
    contract_address = "0xd7bdaa422275eafac364e69ccfb1892bbb0a9c42"
    contract_address = "0x976a67d7ab3870d8c4143915111e4b6a8a813604"
    result = kas_api.get_nft_contract_raw(kas.ChainId.Cypress, contract_address)
    assert result


def test_get_nft(kas_api: kas.KasApi):
    contract_address = "0xd7bdaa422275eafac364e69ccfb1892bbb0a9c42"
    token_id = "0x3a9"
    result = kas_api.get_nft(kas.ChainId.Cypress, contract_address, token_id)
    assert result

    contract_address = "0x976a67d7ab3870d8c4143915111e4b6a8a813604"
    token_id = "0x3a6"
    result = kas_api.get_nft(kas.ChainId.Cypress, contract_address, token_id)
    assert result


def test_get_contracts_by_owner(kas_api: kas.KasApi):
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"
    owner = "0xFE463e0d253Ea6972F13EA93516Da762503d0d2A"
    result = kas_api.get_contracts_by_owner(
        kas.ChainId.Cypress, owner, (kas.TokenKind.NFT,)
    )
    assert result


def test_get_tokens_by_owner(kas_api: kas.KasApi):
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"
    owner = "0xFE463e0d253Ea6972F13EA93516Da762503d0d2A"
    result = kas_api.get_tokens_by_owner_raw(
        kas.ChainId.Cypress, owner, (kas.TokenKind.NFT,)
    )
    assert result
    with open("kas_get_nft_tokens_by_owner.json", "w") as f:
        f.write(json.dumps(result, indent=4))

    result = kas_api.get_tokens_by_owner(
        kas.ChainId.Cypress, owner, (kas.TokenKind.NFT,)
    )
    assert result


def test_update_nft_contract_metadata(kas_api: kas.KasApi):
    contract_address = "0x976a67d7ab3870d8c4143915111e4b6a8a813604"
    result = kas_api.update_nft_contract_metadata(kas.ChainId.Cypress, contract_address)
    assert result


def test_update_nft_token_metadata(kas_api: kas.KasApi):
    token_id = "0x3a6"
    contract_address = "0x976a67d7ab3870d8c4143915111e4b6a8a813604"
    result = kas_api.update_nft_token_metadata(
        kas.ChainId.Cypress, contract_address, token_id
    )
    assert result
