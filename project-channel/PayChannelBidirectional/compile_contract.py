import os
import configparser
from solc import compile_files
from web3 import Web3
import json
OWN_DIR = os.path.dirname(os.path.realpath(__file__))
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def deploy_lib_sign_contract():
    contracts = compile_files([OWN_DIR + '/LibSignatures.sol'])

    # separate main file and link file
    contract_interface = contracts.pop(OWN_DIR + "/LibSignatures.sol:LibSignatures")

    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    # Get transaction hash from deployed contract
    # tx_hash = contract.deploy(
    #     transaction={'from': w3.eth.accounts[1]}
    # )
    tx_hash = contract.constructor().transact()
    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']


def deploy_channel_contract(public_address, i_lib_sign_interface=None):
    if i_lib_sign_interface is None:
        i_lib_sign_interface = deploy_lib_sign_contract()
    print("i_lib_sign_interface ", i_lib_sign_interface)
    contracts = compile_files([OWN_DIR + '/Channel.sol'])

    # separate main file and link file
    contract_interface = contracts.pop(OWN_DIR + "/Channel.sol:Channel")

    # Instantiate and deploy contract
    contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    # Get transaction hash from deployed contract
    # tx_hash = contract.deploy(
    #     transaction={'from': w3.eth.accounts[1]}
    # )
    w3.eth.defaultAccount = public_address
    tx_hash = contract.constructor(i_lib_sign_interface, "0xd7b02e3bDf2EdDBB5793d4728EAfA83EC8C07D0b",
                                   "0xa5547c75B3c989A4fcd6F0456f5AA6E91E3734cf").transact()
    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return tx_receipt['contractAddress']


def get_channel_contract(contract_address):
    # try:
    contracts = compile_files([OWN_DIR + '/Channel.sol'])
    contract_interface = contracts.pop(OWN_DIR + "/Channel.sol:Channel")
    abi = contract_interface['abi']

    contract = w3.eth.contract(
        address=w3.toChecksumAddress(contract_address),
        abi=abi
    )
    return contract, contract_address


flag = False
if flag:
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # library_address = {"ILibSignatures.sol:ILibSignatures": deploy_contract(library_link)}
    # print(library_address)
    # main_contract['bin'] = link_code(main_contract['bin'], library_address)
    lib_sign_interface = "0x405D088963F3b634803C67F47d722608f442ff19"
    channel_contract_address = deploy_channel_contract(i_lib_sign_interface=lib_sign_interface)
    print(channel_contract_address)
