from anv.api import infura


def test_get_nfts(infura_api: infura.InfuraApi):
    # daisy 지갑주소
    owner = "0x90ef80035dF87DE9d211de8E8EE7D3cEE9488619"
    result = infura_api.get_NFTs_by_owner(infura.ChainId.EthereumMain, owner)
    assert result
