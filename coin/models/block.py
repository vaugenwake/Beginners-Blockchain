class Block:
    def __init__(self, miner, transactions, height, difficulty, hash, previous_hash, nonce, timestamp):
        self.miner = miner
        self.transactions = transactions
        self.height = height
        self.difficulty = difficulty
        self.hash = hash
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp
