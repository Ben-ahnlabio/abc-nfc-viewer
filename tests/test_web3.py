import web3


def test_web3_get_balance():
    alchemy_url = (
        "https://eth-mainnet.g.alchemy.com/v2/O06KHzfPbklzwxDp8Z4KDrxIMmazK85c"
    )
    w3 = web3.Web3(web3.Web3.HTTPProvider(alchemy_url))
    assert w3.isConnected()

    balance = w3.eth.get_balance("0x45EB6D727FB8C1EB89284b65D336f2C6bcbA0f73")
    print(balance)


def test_with_test_provider():
    w3 = web3.Web3(web3.EthereumTesterProvider())
    w3.isConnected()
