import configparser
import json
import os

# from web3.auto import w3
from web3 import Web3

OWN_DIR = os.path.dirname(os.path.realpath(__file__))
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))


def deploy_contract(contract_name):
    f = open(OWN_DIR + '/abi.txt', "r")
    contents = f.read()
    f.close()
    abi = json.loads(contents)

    config = configparser.RawConfigParser()
    config.read(OWN_DIR + '/user.properties')

    address = w3.toChecksumAddress(config.get('user', 'address'))
    key = config.get('user', 'key')

    # contract_address = config.get('contract', 'contract_address')
    bytecode = config.get('contract', 'bytecode')

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx = contract.constructor().buildTransaction({
        'from': address,
        'nonce': w3.eth.getTransactionCount(address, 'pending')
    })
    signed = w3.eth.account.signTransaction(tx, key)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print('Successfully deployed {} contract with tx hash {} in contract address {}!'.format(
        contract_name, tx_hash.hex(), tx_receipt.contractAddress))
    return tx_receipt.contractAddress


def get_contract(contract_address=None):
    # try:
    f = open(OWN_DIR + '/abi.txt', "r")
    contents = f.read()
    f.close()
    abi = json.loads(contents)

    # config = configparser.RawConfigParser()
    # config.read(OWN_DIR + '/user.properties')

    # contract_address = config.get('contract', 'contract_address')
    if contract_address is None:
        contract_address = "0x0a42cf87CaDe81e55EF9E9bba6D598720eD09F5e"
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(contract_address),
        abi=abi
    )
    return contract, contract_address


# except:
#     return None

# def signature_testing():
#
#     def add_prefix(message):
#         return '\x19Ethereum Signed Message:\n' + str(len(message)) + message
#
#     def prepare_message(web3, message):
#         return web3.toAscii(web3.sha3(web3.toHex(add_prefix(message))))

# print(get_contract())
if w3.isChecksumAddress(0x42aF249d7e61E304369A485583a093Bf1C9D30bC):
    pass
else:
    public_address = w3.toChecksumAddress(0x42aF249d7e61E304369A485583a093Bf1C9D30bC)
