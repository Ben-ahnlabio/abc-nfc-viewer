from anv import api
from anv.models import NftResponse


def test_klaytn_api_get_nft_by_owner(klaytn_api: api.KlaytnApi):
    # ethan
    owner = "0xf901be601848b31Bc4455d5C405B0FbC2401c9b4"

    # https://opensea.io/Minooong
    owner = "0xFE463e0d253Ea6972F13EA93516Da762503d0d2A"

    # https://pala.io/square/profile?address=0x08cc3fae550f2f57aa85a6fcecfb399716081f2e
    owner = "0x08cc3fae550f2f57aa85a6fcecfb399716081f2e"
    result = klaytn_api.get_NFTs_by_owner(owner)

    response = NftResponse(page=1, per_page=20, items=result)

    assert response
    assert result
