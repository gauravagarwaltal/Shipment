import requests
from ethereum import utils
from web3 import Web3
from web3.auto import w3
import configparser
import json
from eth_keys import keys
from eth_account.messages import encode_defunct


class ChannelState:
    def __init__(self, count, sender_bal, recipient_bal, sign):
        self.count = count
        self.sender_bal = sender_bal
        self.recipient_bal = recipient_bal
        self.sign = sign

    def valid_sign_state(self, count, sender_bal, recipient_bal):
        if self.count == (count - 1):
            if (self.sender_bal + self.recipient_bal) == (int(sender_bal) + int(recipient_bal)):
                return True
            return False
        return False

    def update_state(self, count, sender_bal, recipient_bal, sign):
        self.count = count
        self.sender_bal = sender_bal
        self.recipient_bal = recipient_bal
        self.sign = sign


class User:

    def __init__(self, _contract_address=None, _contract_abi=None, root_chain_provider=None):
        if root_chain_provider is None:
            self.web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
        else:
            self.web3 = Web3(Web3.HTTPProvider(root_chain_provider))
        if _contract_address is None or _contract_abi is None:
            self.contract = None
        else:
            _contract_address = self.web3.toChecksumAddress(_contract_address)
            self.contract = self.web3.eth.contract(address=_contract_address, abi=_contract_abi)
        self.address = None
        self.opponent = None
        self.pri_key = None
        if self.contract is not None:
            count = 0
            sender_bal = self.contract.functions.getBalance().call()
            recipient_bal = self.contract.functions.getRecipientAmount().call()
            self.state = ChannelState(count, sender_bal-recipient_bal, recipient_bal, "sign")
        else:
            self.state = None
        self.pending_requests = dict()

    def add_address(self, public_address, private_key):
        if self.web3.isChecksumAddress(public_address):
            pass
        else:
            public_address = self.web3.toChecksumAddress(public_address)
        private_key = utils.normalize_key(private_key)
        if self.address is not None:
            self.flush_state()
        client = self.contract.functions.getRecipient().call()
        vendor = self.contract.functions.getSender().call()
        if str(public_address).lower() == str(client).lower():
            self.opponent = vendor
            self.address = public_address
            self.pri_key = private_key
        elif str(public_address).lower() == str(vendor).lower():
            self.opponent = client
            self.address = public_address
            self.pri_key = private_key
        else:
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
        return public_address == str(w3.eth.account.recover_message(sender_bal, signature=signed_message.signature)).lower()

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
            return False, False
        else:
            message1 = str(count) + "" + str(sender_bal) + "" + str(recipient_bal)
            message = encode_defunct(text=message1)
            signed_message = w3.eth.account.sign_message(message, private_key=self.pri_key)
            # self.state.update_state(count, sender_bal, recipient_bal, signed_message.signature.hex())
            return signed_message.signature.hex(), True

    def sign_state(self, count, sender_bal, recipient_bal):
        if not self.state.valid_sign_state(count, sender_bal, recipient_bal):
            return False, False
        else:
            message1 = str(count) + "" + str(sender_bal) + "" + str(recipient_bal)
            message = encode_defunct(text=message1)
            signed_message = w3.eth.account.sign_message(message, private_key=self.pri_key)
            return signed_message.signature.hex(), True

    def check_sign(self, count, sender_bal, recipient_bal, signature, account):
        message1 = str(count) + "" + str(sender_bal) + "" + str(recipient_bal)
        message = encode_defunct(text=message1)
        # print(w3.eth.account.recover_message(message, signature=signature))
        print(signature)
        signer = self.contract.functions.verifyString1(message1, signature).call()
        print(signer, account)
        if str(signer).lower() == str(account).lower():
            return True
        else:
            return False

    def get_pending_requests(self):
        return self.pending_requests

    def remove_pending_state(self, key):
        if key in self.pending_requests:
            del self.pending_requests[key]

    def flush_state(self):
        f = open("channel/" + self.address +".properties", "w")
        f.write("count=" + str(self.state.count) + '\n')
        f.write("sender_bal=" + str(self.state.sender_bal) + '\n')
        f.write("recipient_bal=" + str(self.state.recipient_bal) + '\n')
        f.write("sign="+self.state.sign)
        f.close()

    def retrieve_state(self):
    #   TODO: retrieve state and use it (define use cases)
        pass

    def update_contract(self, contract_address, contract_abi):
        contract_address = self.web3.toChecksumAddress(contract_address)
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)


temp_flag = False
if temp_flag:
    config = configparser.RawConfigParser()
    config.read('channel/user.properties')

    contract_address = config.get('contract', 'contract_address')
    contract_abi = config.get('contract', 'contract_abi')
    contract_abi = json.loads(contract_abi)
    object_1 = User(_contract_abi=contract_abi, _contract_address=contract_address)


    object_1.add_address("0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b", "0x740b220f156da692ead7d9e7a1b281534cb90f6821f36628485f1d5a05056be9")
    sign, _bool = (object_1.sign_new_state(1, 5, 6, ))
    print(sign)
    print("check sign ", object_1.check_sign(1, 5, 6, bytes.fromhex(str(sign)[2:]), object_1.address))
    print(object_1.get_state())
    print(object_1.validate_address('0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b', '0x740b220f156da692ead7d9e7a1b281534cb90f6821f36628485f1d5a05056be9'))
    print(object_1.contract.functions.getRecipient().call())
    print(object_1.contract.functions.getSender().call())