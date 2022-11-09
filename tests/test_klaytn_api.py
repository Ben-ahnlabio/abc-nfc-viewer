from anv import api


def test_klaytn_api_get_nft_by_owner(klaytn_api: api.KlaytnApi):
    # ethan
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"

    # https://opensea.io/Minooong
    owner = "0xFE463e0d253Ea6972F13EA93516Da762503d0d2A"
    result = klaytn_api.get_NFTs_by_owner(owner)

    assert result
