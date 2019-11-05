import configparser
import os

from eth_account.messages import encode_defunct
from web3 import Web3
from web3.auto import w3

from PayChannelBidirectional.ChannelState import ChannelState
from PayChannelBidirectional.ChannelStatusMapping import get_status
from PayChannelBidirectional.SigConverter import get_byte_sign, get_hex_sign
from PayChannelBidirectional.compile_contract import deploy_channel_contract, get_channel_contract

OWN_DIR = os.path.dirname(os.path.realpath(__file__))


class ChannelClass:

    def __init__(self, _address, _key, _contract_address, root_chain_provider=None):
        if root_chain_provider is None:
            self.web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
        else:
            self.web3 = Web3(Web3.HTTPProvider(root_chain_provider))

        self.contract, self.contract_address = get_channel_contract(_contract_address)
        self.address = self.web3.toChecksumAddress(_address)
        self.pri_key = _key
        self.opponent = None
        self.state = ChannelState("", "", "", "")
        self.pending_requests = dict()

    def set_state(self):
        try:
            self.state = ChannelState("", "", "", "")
            count = 0
            alice_id, alice_cash, alice_flag = self.contract.functions.alice().call()
            bob_id, bob_cash, bob_flag = self.contract.functions.bob().call()
            flag = self.retrieve_state()
            if str(alice_id).lower() == str(self.address).lower():
                self.opponent = self.web3.toChecksumAddress(bob_id)
                if not flag:
                    self.state = ChannelState(count, int(alice_cash), int(bob_cash), "genesis")
            else:
                self.opponent = self.web3.toChecksumAddress(alice_id)
                if not flag:
                    self.state = ChannelState(count, int(bob_cash), int(alice_cash), "genesis")
        except:
            pass

    def get_balance(self, public_address):
        try:
            if self.web3.isChecksumAddress(public_address):
                return self.web3.eth.getBalance(public_address)
            else:
                public_address = self.web3.toChecksumAddress(public_address)
                return self.web3.eth.getBalance(public_address)
        except:
            return None

    @staticmethod
    def validate_address(public_address, private_key):
        sender_bal = encode_defunct(text="sender_balance")
        signed_message = w3.eth.account.sign_message(sender_bal, private_key=private_key)
        return public_address == str(
            w3.eth.account.recover_message(sender_bal, signature=signed_message.signature)).lower()

    def get_block(self, count, sender_balance, recipient_bal):
        # try:
        message = str(count) + "" + str(sender_balance) + "" + str(recipient_bal)

        sender_bal = encode_defunct(text=sender_balance)

        # hash_value = self.web3.keccak(text=sender_bal)
        # print("hash_value ", hash_value.hex())

        signed_message = w3.eth.account.sign_message(sender_bal, private_key=self.key)
        print("signature ", signed_message)

        # print(w3.eth.account.recover_message(sender_bal, signature=signed_message.signature))
        print("message hash ", signed_message.messageHash)
        # print(self.contract.functions.isValidSignature(str(count), str(sender_bal), str(recipient_bal), v, r, s).call())

        print(self.contract.functions.isValidSignature(sender_balance, signed_message.signature).call())

        print(self.contract.functions.recover(signed_message.messageHash, signed_message.signature).call())

    def get_state(self):
        response = {'count': self.state.count, 'sender_bal': self.state.sender_bal,
                    'recipient_bal': self.state.recipient_bal, 'sign': self.state.sign}
        return response

    def sign_new_state(self, count, sender_bal, recipient_bal):
        if not self.state.valid_sign_state(count, sender_bal, recipient_bal):
            return False
        else:
            message_bytes = (w3.soliditySha3(['uint256', 'uint256', 'uint256'],
                                             [int(count), int(sender_bal), int(recipient_bal)]))
            prefixed_msg = encode_defunct(hexstr=message_bytes.hex())
            signed_message = w3.eth.account.sign_message(prefixed_msg, private_key=self.pri_key)
            return signed_message.signature.hex()

    def sign_state(self, count, sender_bal, recipient_bal):
        message_bytes = (w3.soliditySha3(['uint256', 'uint256', 'uint256'],
                                         [int(count), int(sender_bal), int(recipient_bal)]))
        prefixed_msg = encode_defunct(hexstr=message_bytes.hex())
        signed_message = w3.eth.account.sign_message(prefixed_msg, private_key=self.pri_key)
        return signed_message.signature.hex()

    def check_sign(self, count, sender_bal, recipient_bal, signature, account):
        # solidity function signature return boolean value
        # isValidSignature(address addr, uint count, uint sender_balance, uint recipient_balance, bytes signature)
        flag = self.contract.functions.isValidSignature(self.web3.toChecksumAddress(account), int(count),
                                                        int(sender_bal), int(recipient_bal),
                                                        get_byte_sign(signature)).call()
        return flag

    def get_pending_requests(self):
        return self.pending_requests

    def remove_pending_state(self, key):
        if key in self.pending_requests:
            del self.pending_requests[key]

    def flush_state(self):
        if not os.path.exists(self.address):
            os.makedirs(self.address)
        config = configparser.RawConfigParser()
        config.read(self.address + '/' + self.contract_address + ".properties")
        if not config.has_section("channel"):
            config.add_section("channel")
        config.set("channel", "count", str(self.state.count))
        config.set("channel", "sender_bal", str(self.state.sender_bal))
        config.set("channel", "recipient_bal", str(self.state.recipient_bal))
        config.set("channel", "sign", get_hex_sign(self.state.sign))
        file = open(self.address + '/' + self.contract_address + ".properties", 'w')
        config.write(file)
        file.close()

    def retrieve_state(self):
        if os.path.exists(self.address + '/' + self.contract_address + ".properties"):
            config = configparser.RawConfigParser()
            config.read(self.address + '/' + self.contract_address + ".properties")

            count = int(config.get('channel', 'count'))
            sender_bal = int(config.get('channel', 'sender_bal'))
            recipient_bal = int(config.get('channel', 'recipient_bal'))
            sign = config.get('channel', 'sign')
            self.state.update_state(count, sender_bal, recipient_bal, sign)
            return True
        else:
            return False

    def update_contract(self):
        contract_address = deploy_channel_contract(self.address,
                                                   i_lib_sign_interface="0x0662B997813b9e35dFCC0bBf65C42729c5AD5770")
        contract_address = self.web3.toChecksumAddress(contract_address)
        # self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        self.contract, self.contract_address = get_channel_contract(contract_address)

    def get_channel_details(self):
        channel_contract_address = self.contract_address
        status = get_status(self.contract.functions.status().call())
        alice_id, alice_cash, alice_input = self.contract.functions.alice().call()
        bob_id, bob_cash, bob_input = self.contract.functions.bob().call()
        if self.web3.toChecksumAddress(alice_id) == self.web3.toChecksumAddress(self.address):
            payload = {'CA': channel_contract_address, 'aliceId': alice_id, 'aliceCash': alice_cash,
                       'aliceInput': alice_input, 'bobId': bob_id, 'bobCash': bob_cash, 'bobInput': bob_input,
                       'status': status}
            return payload
        else:
            payload = {'CA': channel_contract_address, 'aliceId': bob_id, 'aliceCash': bob_cash,
                       'aliceInput': bob_input, 'bobId': alice_id, 'bobCash': alice_cash, 'bobInput': alice_input,
                       'status': status}
            return payload

    def confirm_input(self, amount):
        tx = self.contract.functions.confirm().transact({'from': self.address, 'value': amount})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)
        return tx_receipt

    def refund(self):
        if int(self.contract.functions.timeout().call()) == 0:
            return None
        tx = self.contract.functions.refund().transact({'from': self.address})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)
        return tx_receipt

    def close_channel(self):
        tx = self.contract.functions.close(int(self.state.count), int(self.state.sender_bal),
                                           int(self.state.recipient_bal), get_byte_sign(self.state.sign)).transact(
            {'from': self.address})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)
        return tx_receipt

    def finalize_close(self):
        if int(self.contract.functions.timeout().call()) == 0:
            return None
        tx = self.contract.functions.finalizeClose().transact({'from': self.address})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx)
        return tx_receipt


temp_flag = False
if temp_flag:
    print("testing class")
    # config = configparser.RawConfigParser()
    # config.read('channel/user.properties')
    #
    # contract_address = config.get('contract', 'contract_address')
    # contract_abi = config.get('contract', 'contract_abi')
    # contract_abi = json.loads(contract_abi)
    contract_address = "0x7AA1aa46A5c91CF85FC5A7D0Cc8669fbAAA93892"
    user = ChannelClass(_address="0xa5547c75b3c989a4fcd6f0456f5aa6e91e3734cf",
                        _key="0x1bb00ed95652a818ff64043d9f098bbd637c5c90aae597eac4ea8f9f089e7c99",
                        _contract_address=contract_address)
    user.close_channel(2, 20, 0,
                       b'\xbd\x94\xc0\xb1n\xf8\x19\xfa\r\x7f;h\x92X\xfeD&I\xabCI\xb4\x03~\xc7\xa1S\xa6\xceM\x8fF]-\x06q\xeeG\x04w\x9c\xd3\xa4\xfcD\x81b"\xa8\xbf\xfcN\x8f\xae\xa4\n\xc8u\x82B\x9b8\xae]\x1b')
    #
    #
    # object_1.add_address("0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b", "0x740b220f156da692ead7d9e7a1b281534cb90f6821f36628485f1d5a05056be9")
    # sign, _bool = (object_1.sign_new_state(1, 5, 6, ))
    # print(sign)
    # print("check sign ", object_1.check_sign(1, 5, 6, bytes.fromhex(str(sign)[2:]), object_1.address))
    # print(object_1.get_state())
    # print(object_1.validate_address('0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b', '0x740b220f156da692ead7d9e7a1b281534cb90f6821f36628485f1d5a05056be9'))
    # print(object_1.contract.functions.getRecipient().call())
    # print(object_1.contract.functions.getSender().call())
