import json
import os

# from web3.auto import w3
from web3 import Web3

OWN_DIR = os.path.dirname(os.path.realpath(__file__))
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))


def get_contract_instance():
    f = open(OWN_DIR + '/contract_abi.txt', "r")
    contents = f.read()
    f.close()
    abi = json.loads(contents)

    # config = configparser.RawConfigParser()
    # config.read(OWN_DIR + '/user.properties')

    # contract_address = config.get('contract', 'contract_address')
    contract_address = "0x19DbcfB1E970EB0ac300936824de350EE248e803"
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(contract_address),
        abi=abi
    )
    return contract
