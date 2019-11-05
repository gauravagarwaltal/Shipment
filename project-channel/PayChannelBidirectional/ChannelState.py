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
