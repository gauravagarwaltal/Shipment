from eth_account.messages import encode_defunct
from web3.auto import w3


def get_byte_sign(signature):
    try:
        byte_sign = bytes.fromhex(signature)
        return byte_sign
    except:
        try:
            byte_sign = bytes.fromhex(str(signature)[2:])
            return byte_sign
        except:
            return signature


def get_hex_sign(signature):
    try:
        hex_sign = bytes(signature).hex()
        return hex_sign
    except:
        return signature


flag = False
if flag:
    public_address = "0xa5547c75b3c989a4fcd6f0456f5aa6e91e3734cf",
    private_key = "0x1bb00ed95652a818ff64043d9f098bbd637c5c90aae597eac4ea8f9f089e7c99"
    sender_bal = encode_defunct(text="sender_balance")
    signed_message = w3.eth.account.sign_message(sender_bal, private_key=private_key)
    _sign = signed_message.signature.hex()
    print(signed_message.signature, _sign)
    print("\n---byte sign func---")
    print(get_byte_sign("bd94c0b16ef819fa0d7f3b689258fe442649ab4349b4037ec7a153a6ce4d8f465d2d0671ee4704779cd3a4fc44816222a8bffc4e8faea40ac87582429b38ae5d1b"))
    print("\n---hex sign func---")
    print(get_hex_sign(get_byte_sign(_sign)))
