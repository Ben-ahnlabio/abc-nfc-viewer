import json

from anv.api import alchemy


def test_alchemy_get_NFTs_raw(alchemy_api: alchemy.AlchemyApi):
    # result = api.get_NFTs("0x45EB6D727FB8C1EB89284b65D336f2C6bcbA0f73")
    # assert result
    # daisy 지갑주소
    result = alchemy_api.get_NFTs_raw(
        alchemy.AlchemyNet.EthMainNet,
        "0x90ef80035dF87DE9d211de8E8EE7D3cEE9488619",
    )

    # https://opensea.io/punksOTC2
    result = alchemy_api.get_NFTs_raw(
        alchemy.AlchemyNet.EthMainNet,
        "0x0232d1083E970F0c78f56202b9A666B526FA379F",
    )
    assert result
    with open("alchemy_get_nfts_result.json", "w") as f:
        f.write(json.dumps(result))


def test_alchemy_get_NFTs(alchemy_api: alchemy.AlchemyApi):
    # result = api.get_NFTs("0x45EB6D727FB8C1EB89284b65D336f2C6bcbA0f73")
    # assert result
    # daisy 지갑주소
    result = alchemy_api.get_NFTs(
        alchemy.AlchemyNet.EthMainNet,
        "0x90ef80035dF87DE9d211de8E8EE7D3cEE9488619",
    )
    assert result

    # https://opensea.io/punksOTC2
    result = alchemy_api.get_NFTs(
        alchemy.AlchemyNet.EthMainNet,
        "0x0232d1083E970F0c78f56202b9A666B526FA379F",
    )
    assert result


def test_alchemy_get_NFT_metadata(alchemy_api: alchemy.AlchemyApi):
    # result = alchemy_api.get_NFT_metadata("0x2931b181ae9dc8f8109ec41c42480933f411ef94")
    result = alchemy_api.get_NFT_metadata(
        alchemy.AlchemyNet.EthMainNet,
        "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
        token_id="0x0f59",
    )
    assert result


def test_alchemy_get_NFT_metadata_raw(alchemy_api: alchemy.AlchemyApi):
    # result = alchemy_api.get_NFT_metadata_raw(
    #     alchemy.AlchemyNet.EthMainNet,
    #     "0x2931b181ae9dc8f8109ec41c42480933f411ef94",
    #     token_id="0x0000000000000000000000000000000000000000000000000000000000000262",
    # )

    result = alchemy_api.get_NFT_metadata_raw(
        alchemy.AlchemyNet.EthMainNet,
        "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb",
        token_id="0x0f59",
    )

    assert result
    with open("alchemy_nft_metadata.json", "w") as f:
        f.write(json.dumps(result))


def test_alchemy_get_contract_metadata(alchemy_api: alchemy.AlchemyApi):
    # hood daisy
    contract_address = "0x2931b181ae9dc8f8109ec41c42480933f411ef94"
    contract_address = "0x039b52db88ae51b86b7ab091fa710082ef60dd7b"
    contract_address = "0x008C69E0c66EbD4b228D27F2162aD54AB1b7dDE1"
    result = alchemy_api.get_contract_metadata(
        alchemy.AlchemyNet.EthMainNet, contract_address
    )
    assert result
    with open("alchemy_contract_metadata.json", "w") as f:
        f.write(json.dumps(result))
