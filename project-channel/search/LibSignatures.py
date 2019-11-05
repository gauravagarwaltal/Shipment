import configparser
import os

from eth_account.messages import encode_defunct
from ethereum import utils
from web3 import Web3
from web3.auto import w3

from search.contract_instance import get_contract


class LibSignatures:

    def __init__(self, pub_address, secret_key):
        self.web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
        self.contract = get_contract()
        self.address = pub_address
        self.pri_key = secret_key

    def add_address(self, public_address, private_key):
        if self.web3.isChecksumAddress(public_address):
            pass
        else:
            public_address = self.web3.toChecksumAddress(public_address)
        private_key = utils.normalize_key(private_key)
        self.address = public_address
        self.pri_key = private_key

    def get_balance(self):
        public_address = self.address
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

    def get_block(self):
        # try:
        message = "xyz"

        sender_bal = encode_defunct(text=message)

        signed_message = w3.eth.account.sign_message(sender_bal, private_key=self.pri_key)
        print("signature ", signed_message)

        # print(w3.eth.account.recover_message(sender_bal, signature=signed_message.signature))
        print("message hash ", signed_message.messageHash)

        print("getNOw ", self.contract.functions.getNow().call())
        print(self.contract.functions.verify(self.address, signed_message.messageHash, signed_message.signature).call())

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

    def update_contract(self):
        # self.contract = get_contract()
        vid = 5
        p1 = w3.toChecksumAddress("0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b")
        message_bytes = (w3.soliditySha3(['uint256', 'address', 'uint256', 'uint256', 'address', 'uint256'],
                                         [vid, p1, vid, vid, p1, vid]))

        # message_bytes = (w3.soliditySha3(['bytes', 'bytes32'],
        #                                  [bytes.fromhex("\x19Ethereum Signed Message:\n32"), message_bytes]))
        # bytes memory prefix = "\x19Ethereum Signed Message:\n32";
        # bytes32 prefixedHash = keccak256(prefix, hash);

        # print(w3.keccak(str(vid) + p1 + str(cash1) + str(subchan1) + ingrid + str(version)))
        signature = self.web3.eth.sign(self.address, data=message_bytes)
        sender_bal = encode_defunct(hexstr=message_bytes.hex())

        signed_message = w3.eth.account.sign_message(sender_bal, private_key=self.pri_key)
        # print("signature ", signed_message)
        # print(w3.eth.account.recover_message(sender_bal, signature=signed_message.signature))

        print("hello ",
              self.contract.functions.verify(self.address, signed_message.messageHash, signed_message.signature).call())
        print("Mic Check ",
              self.contract.functions.CheckSignature(self.address, vid, p1, vid, vid, p1, vid,
                                                     signed_message.signature).call())


temp_flag = True
if temp_flag:
    OWN_DIR = os.path.dirname(os.path.realpath(__file__))
    config = configparser.RawConfigParser()
    config.read(OWN_DIR + '/user.properties')

    address = w3.toChecksumAddress(config.get('user', 'address'))
    key = config.get('user', 'key')

    # object_1 = LibSignatures(address, key)

    # print(object_1.get_balance())
    # object_1.get_block()
    # object_1.update_contract()

