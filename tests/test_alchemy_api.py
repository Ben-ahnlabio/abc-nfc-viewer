import json

from anv.api import alchemy


def test_alchemy_get_NFTs(alchemy_api: alchemy.AlchemyApi):
    # result = api.get_NFTs("0x45EB6D727FB8C1EB89284b65D336f2C6bcbA0f73")
    # assert result
    # daisy 지갑주소
    result = alchemy_api.get_NFTs(
        alchemy.AlchemyNetwork.EthereumMainNet,
        "0x90ef80035dF87DE9d211de8E8EE7D3cEE9488619",
    )

    # https://opensea.io/punksOTC2
    result = alchemy_api.get_NFTs(
        alchemy.AlchemyNetwork.EthereumMainNet,
        "0x0232d1083E970F0c78f56202b9A666B526FA379F",
    )
    assert result
    with open("result.json", "w") as f:
        f.write(json.dumps(result))


def test_alchemy_get_NFT_metadata(alchemy_api: alchemy.AlchemyApi):
    # result = alchemy_api.get_NFT_metadata("0x2931b181ae9dc8f8109ec41c42480933f411ef94")
    result = alchemy_api.get_NFT_metadata(
        alchemy.AlchemyNetwork.EthereumMainNet,
        "0x2931b181ae9dc8f8109ec41c42480933f411ef94",
        token_id="0x0000000000000000000000000000000000000000000000000000000000000262",
    )
    assert result
    with open("nft_metadata.json", "w") as f:
        f.write(json.dumps(result))
