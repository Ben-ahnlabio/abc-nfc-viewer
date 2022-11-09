from anv import api


def test_ethreum_api_get_nft_by_owner(ethereum_api: api.EthereumApi):
    # daisy
    # owner = "0x90ef80035dF87DE9d211de8E8EE7D3cEE9488619"
    # many
    owner = "0x0232d1083E970F0c78f56202b9A666B526FA379F"
    # ricepotato
    # owner = "0x45EB6D727FB8C1EB89284b65D336f2C6bcbA0f73"
    result = ethereum_api.get_NFTs_by_owner(owner)
    assert result
