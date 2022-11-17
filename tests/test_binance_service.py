from anv import service


def test_binance_service_get_nfts(binance_nft_service: service.BinanceNFTService):
    # nft 35만
    owner = "0xe0a9e5b59701a776575fdd6257c3f89ae362629a"
    owner = "0x609306d8890904a0019997585018b70c8c4e1fea"
    nfts = binance_nft_service.get_NFTs_by_owner(owner)
    assert nfts
