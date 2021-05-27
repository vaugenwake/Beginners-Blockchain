class Transaction:
    def __init__(self, hash, sender, reciever, signature, timestamp, amount):
        self.hash = hash
        self.sender = sender
        self.reciever = reciever
        self.signature = signature
        self.timestamp = timestamp
        self.amount = amount
