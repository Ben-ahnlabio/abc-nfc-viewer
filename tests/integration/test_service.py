import pytest
from anv import service
from anv.api import alchemy


def test_binance_service_get_nfts(binance_nft_service: service.BinanceNFTService):
    # nft 35만
    owner = "0xe0a9e5b59701a776575fdd6257c3f89ae362629a"
    owner = "0x308318B98B48C1fdfa72efd0BD3F5233c4b45AA9"
    nfts1 = binance_nft_service.get_NFTs_by_owner(owner, resync=True)
    assert nfts1
    # nfts2 = binance_nft_service.get_NFTs_by_owner(owner, cursor=nfts1.cursor)
    # assert nfts2


def test_binance_service_get_nft_contract_token_id(
    binance_nft_service: service.BinanceNFTService,
):
    contract_address = "0xd832275179f2c19b5ec02c673d7bcebfd87a8c01"
    token_id = "215600019204"

    result = binance_nft_service.get_NFT_by_contract_token_id(
        contract_address=contract_address, token_id=token_id, resync=True
    )
    assert result

    result = binance_nft_service.get_NFT_by_contract_token_id(
        contract_address=contract_address, token_id=token_id, resync=False
    )
    assert result


def test_klaytn_service_get_nfts(klaytn_nft_service: service.KlaytnNFTService):
    owner = "0x0E9bC621207f12FF37589a2f234b7D1a920De117"
    owner = "0x03E5ecA4B61412A5ece56928318d00c3b5567ef8"
    nfts1 = klaytn_nft_service.get_NFTs_by_owner(owner)
    assert nfts1

    nfts2 = klaytn_nft_service.get_NFTs_by_owner(owner, cursor=nfts1.cursor)
    assert nfts2

    nfts3 = klaytn_nft_service.get_NFTs_by_owner(owner, cursor=nfts2.cursor)
    assert nfts3


def test_klaytn_service_get_nft_contract_token_id(
    klaytn_nft_service: service.KlaytnNFTService,
):
    contract_address = "0x77777777777b7fdaa2fceb47ebde85cd461f8859"
    token_id = "0x7a7"

    result = klaytn_nft_service.get_NFT_by_contract_token_id(
        contract_address=contract_address, token_id=token_id, resync=True
    )
    assert result


def test_ethereum_service_get_nfts(ethereum_nft_service: service.EthereumNFTService):
    owner = "0x2488f090656BddB63fe3Bdb506D0D109AaaD93Bb"
    nfts1 = ethereum_nft_service.get_NFTs_by_owner(owner)
    assert nfts1
    nfts2 = ethereum_nft_service.get_NFTs_by_owner(owner, cursor=nfts1.cursor)
    assert nfts2


def test_ethereum_service_get_nft_contract_token_id(
    ethereum_nft_service: service.EthereumNFTService,
):
    contract_address = "0x1df456a9d11b00475b9adf627a330485d0fed607"
    token_id = "0x018d"

    result = ethereum_nft_service.get_NFT_by_contract_token_id(
        contract_address=contract_address, token_id=token_id, resync=True
    )
    assert result

    result = ethereum_nft_service.get_NFT_by_contract_token_id(
        contract_address=contract_address, token_id=token_id, resync=False
    )
    assert result


def test_polygon_service_get_nfts(polygon_nft_service: service.PolygonNFTService):
    owner = "0x609306d8890904a0019997585018b70c8c4e1fea"
    nfts1 = polygon_nft_service.get_NFTs_by_owner(owner)
    assert nfts1
    nfts2 = polygon_nft_service.get_NFTs_by_owner(owner, cursor=nfts1.cursor)
    assert nfts2


def test_polygon_service_get_nft_contract_invalid_token_id(
    polygon_nft_service: service.PolygonNFTService,
):
    contract_address = "0xe013a4dd240b4e4821148ff786cfa050d60182bb"
    token_id = "0x10f"

    with pytest.raises(alchemy.AlchemyApiError):
        polygon_nft_service.get_NFT_by_contract_token_id(
            contract_address=contract_address, token_id=token_id, resync=True
        )
