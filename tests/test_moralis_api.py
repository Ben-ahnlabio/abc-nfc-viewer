import json
from anv.api import moralis


def test_moralis_get_nfts(moralis_api: moralis.MorailsApi):
    # bsc wallet address
    owner = "0xB94Bcff97C4d7379150AB35D8d2dA2D97a83433B"

    result = moralis_api.get_NFTs_raw(moralis.MorailsNetwork.BinanceMainNet, owner)
    assert result
    with open("moralis_nfts_by_owner.json", "w") as f:
        f.write(json.dumps(result))


def test_get_moralis_get_nft_metadata(moralis_api: moralis.MorailsApi):
    contract_address = "0x25Dc4d9e2598c21DC020aa7B741377eCde971C2f"
    token_id = "723"

    result = moralis_api.get_NFT_metadata_raw(
        moralis.MorailsNetwork.BinanceMainNet, contract_address, token_id
    )
    assert result
    with open("moralis_nft_metadata.json", "w") as f:
        f.write(json.dumps(result))
