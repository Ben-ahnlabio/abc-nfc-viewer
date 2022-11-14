import web3


def test_get_erc_721_nft_metadata_from_contract_address_using_web3(web3_obj: web3.Web3):
    # ERC-721
    # erc_721_api
    erc_721_abi = [
        {
            "inputs": [
                {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
            ],
            "name": "tokenURI",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "baseURI",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
            ],
            "name": "ownerOf",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    assert web3_obj.isConnected()

    # BAYC contract address
    tokenContract = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
    checksum_addr = web3.Web3.toChecksumAddress(tokenContract)
    tokenId = 101  # A token we'd like to retrieve its metadata of

    contract = web3_obj.eth.contract(address=checksum_addr, abi=erc_721_abi)
    assert contract
    token_uri = contract.functions.tokenURI(tokenId).call()
    assert token_uri
    base_uri = contract.functions.baseURI().call()
    assert base_uri
    name = contract.functions.name().call()
    assert name
    owner = contract.functions.owner().call()
    assert owner


def test_get_erc_1155_nft_metadata_from_contract_address_using_web3(
    web3_obj: web3.Web3,
):
    # ERC-1155
    erc_1155_abi = [
        {
            "inputs": [],
            "name": "name",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}],
            "name": "uri",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
    ]

    assert web3_obj.isConnected()

    # BAYC contract address
    tokenContract = "0x495f947276749ce646f68ac8c248420045cb7b5e"
    tokenContract = "0x77f278961ac1ea804ee70be8fc30dd2697f720ce"
    checksum_addr = web3.Web3.toChecksumAddress(tokenContract)
    tokenId = 0x01

    # contract = web3_obj.eth.Contract(tokenURIABI, tokenContract)

    contract = web3_obj.eth.contract(address=checksum_addr, abi=erc_1155_abi)
    assert contract

    name = contract.functions.name().call()
    assert name

    uri = contract.functions.uri(tokenId).call()
    assert uri


def test_get_nft_transactions(web3_obj: web3.Web3):
    owner = "0x90ef80035dF87DE9d211de8E8EE7D3cEE9488619"

    latest_block = web3_obj.eth.get_block("latest")

    transaction = web3_obj.eth.get_transaction(
        "0x2785bcc3be56ad1d05e127c38a3b6fb6e8ffd7f5b6f23a2ffca3d050c726be21"
    )
    assert transaction
