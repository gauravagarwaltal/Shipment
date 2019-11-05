import json
import os

from web3 import Web3

OWN_DIR = os.path.dirname(os.path.realpath(__file__))
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))


class ServerHandler:
    def __init__(self):
        self.address_socket_mapping = dict()
        self.address_id_mapping = dict()
        self.address_request_mapping = dict()
        self.address_response_mapping = dict()

    def read_address_id_mapping(self):
        with open(OWN_DIR + '/address_id_mapping.txt', 'r') as f:
            data = f.read()
            self.address_id_mapping = data
            print(self.address_id_mapping)
            # do something with data

    def write_address_id_mapping(self):
        with open(OWN_DIR + '/address_id_mapping.txt', 'w') as f:
            json.dump(self.address_id_mapping, f)

    def get_listening_address(self, address):
        return self.address_socket_mapping.get(web3.toChecksumAddress(address))

    def update_listening_address(self, address, listening_address):
        self.address_socket_mapping[web3.toChecksumAddress(address)] = listening_address

    def get_channels_by_address(self, address):
        return self.address_id_mapping.get(web3.toChecksumAddress(address))

    def update_channel_id(self, channel_id):
        # TODO: call contract and get channel id details and updates details accordingly
        pass

    def get_request_by_address(self, address):
        return self.address_request_mapping.get(web3.toChecksumAddress(address))

    def update_request_by_address(self, address, channel_id, count, alice_cash, bob_cash, signature):
        # TODO: call contract and get channel id details and updates details accordingly
        pass

    def get_response_by_address(self, address):
        return self.address_response_mapping.get(web3.toChecksumAddress(address))

    def update_response_by_address(self, address, channel_id, count, alice_cash, bob_cash, signature):
        # TODO: call contract and get channel id details and updates details accordingly
        pass