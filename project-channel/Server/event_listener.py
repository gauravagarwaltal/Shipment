import json
import os
import time

# from web3.auto import w3
from web3 import Web3

OWN_DIR = os.path.dirname(os.path.realpath(__file__))
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# contractAddress = '0x345ca3e014aaf5dca488057592ee47305d9b3e10'
# contract = w3.eth.contract(address=contractAddress, abi=abiJson['abi'])
# accounts = w3.eth.accounts


def handle_event(event):
    print(event)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)





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


def event_listener_handler():
    f = open(OWN_DIR + '/contract_abi.txt', "r")
    contents = f.read()
    f.close()
    abi = json.loads(contents)

    # config = configparser.RawConfigParser()
    # config.read(OWN_DIR + '/user.properties')

    # contract_address = config.get('contract', 'contract_address')
    contract_address = "0x19DbcfB1E970EB0ac300936824de350EE248e803"
    contract_instance = w3.eth.contract(
        address=w3.toChecksumAddress(contract_address),
        abi=abi
    )
    block_filter = w3.eth.filter({'fromBlock': 0, 'address': contract_address})
    log_loop(block_filter, 2)

    # while True:
    #     for event in contract_instance.eventFilter('EventClosed', {'fromBlock': 0}).get_new_entries():
    #         print(event)
    # print(contract_instance.functions.emitLog().call())
    # myfilter = contract_instance.events.EventClosed.createFilter(fromBlock=0)
    # eventlist = myfilter.get_all_entries()
    # print(eventlist)
    #
    # myfilter = contract_instance.events.EventInitializing.createFilter(fromBlock=0)
    # eventlist = myfilter.get_all_entries()
    # print(eventlist)


event_listener_handler()
