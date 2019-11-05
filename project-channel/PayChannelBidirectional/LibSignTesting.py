import os

from eth_account.messages import encode_defunct
from solc import compile_files
from web3 import Web3

# from ethereum import utils

OWN_DIR = os.path.dirname(os.path.realpath(__file__))
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def lib_sign_contract_instance():
    contracts = compile_files([OWN_DIR + '/LibSignatures.sol'])

    # separate main file and link file
    contract_interface = contracts.pop(OWN_DIR + "/LibSignatures.sol:LibSignatures")
    _contract_address = "0x405D088963F3b634803C67F47d722608f442ff19"
    contract = w3.eth.contract(
        address=w3.toChecksumAddress(_contract_address),
        abi=contract_interface['abi']
    )
    return contract


w3.eth.defaultAccount = w3.eth.accounts[0]

contract_instance = lib_sign_contract_instance()

print("\n---testing of signature using prefix and not using prefix")
vid = 5
p1 = w3.toChecksumAddress("0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b")
pri_key = ("0x740b220f156da692ead7d9e7a1b281534cb90f6821f36628485f1d5a05056be9")
message_bytes = (w3.soliditySha3(['uint256', 'address', 'uint256', 'uint256', 'address', 'uint256'],
                                 [vid, p1, vid, vid, p1, vid]))

print("\nbytes of int add int -> ", message_bytes)

print("\ncheck Hash ", contract_instance.functions.checkHash(vid, p1, vid, vid, p1, vid).call())

prefixed_msg = encode_defunct(hexstr=message_bytes.hex())

signed_message = w3.eth.account.sign_message(prefixed_msg, private_key=pri_key)
# print("signature ", signed_message)
# print(w3.eth.account.recover_message(sender_bal, signature=signed_message.signature))

print("\nhello ",
      contract_instance.functions.verify(p1, signed_message.messageHash, signed_message.signature).call())
print("\nMic Check ",
      contract_instance.functions.CheckSignature(p1, vid, p1, vid, vid, p1, vid,
                                                 signed_message.signature).call())
