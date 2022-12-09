import os

import web3


class KaytnWeb3:
    def __init__(self):
        self.KLAYTN_CYPRESS_WEB3_RPC_URL = os.getenv("KLAYTN_CYPRESS_WEB3_RPC_URL")
        self.KLAYTN_BAOBAB_WEB3_RPC_URL = os.getenv("KLAYTN_BAOBAB_WEB3_RPC_URL")

    def get_nft_contract_name(self, contract_address: str) -> str:
        abi = [
            {
                "inputs": [],
                "name": "name",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function",
            },
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
                "constant": True,
                "inputs": [{"name": "", "type": "uint256"}],
                "name": "uri",
                "outputs": [{"name": "", "type": "string"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
        ]

        checksum_addr = web3.Web3.toChecksumAddress(contract_address)
        web3_obj = web3.Web3(web3.Web3.HTTPProvider(self.KLAYTN_CYPRESS_WEB3_RPC_URL))
        contract = web3_obj.eth.contract(address=checksum_addr, abi=abi)

        get_name_func = contract.get_function_by_name("name")
        return get_name_func().call()
