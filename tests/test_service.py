from anv import service


def test_binance_service_get_nfts(binance_nft_service: service.BinanceNFTService):
    # nft 35만
    owner = "0xe0a9e5b59701a776575fdd6257c3f89ae362629a"
    owner = "0x609306d8890904a0019997585018b70c8c4e1fea"
    nfts = binance_nft_service.get_NFTs_by_owner(owner)
    assert nfts


def test_klaytn_service_get_nfts(klaytn_nft_service: service.KlaytnNFTService):
    owner = "0x03E5ecA4B61412A5ece56928318d00c3b5567ef8"
    nfts = klaytn_nft_service.get_NFTs_by_owner(owner)
    assert nfts


def test_ethereum_service_get_nfts(ethereum_nft_service: service.EthereumNFTService):
    owner = "0x2488f090656BddB63fe3Bdb506D0D109AaaD93Bb"
    nfts = ethereum_nft_service.get_NFTs_by_owner(owner)
    assert nfts
