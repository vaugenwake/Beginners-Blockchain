import hashlib
import json
from time import time

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Start the blockchain with a genesis block
        self.new_block(previous_hash=1, proof=100)

    """
    Create a new Block in the Blockchain
    :param proof: <int> The proof given by the Proof of Work
    :param previous_hash: (Optional) <str> Hash of previous Block
    :return <dict> New Block
    """
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        
        # Reset the current list of transactions
        self.current_transactions = []

        # Add the block to the chain
        self.chain.append(block)
        return block

    """
    Creates a new transaction to go into the next mined Block
    :param sender <str> Address of the sender
    :param recipient <str> Address of the recipient
    :param amount: <int> Amount being sent
    :return <int> The index of the Block that will hold this transaction
    """
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    """
    Create a SHA-256 hash of a Block
    :param block: <dict> Block
    :return <str>
    """
    @staticmethod
    def hash(block):
        # Make sure the dictionary is in the same order always or hashes will be inconsistent.
        block_string = json.dumps(block, sort_keys=True).encode();
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains a leading 4 zeros, where p, is the pervious p'
    - p is the previous proof, and p' is the new proof
    :param last_proof: <int>
    :return <int>
    """
    def proof_of_work(self, last_proof):
        proof = 0

        # Keep solving proof until computation is complete.
        while self.valid_proof(last_proof=last_proof, proof=proof) is False:
            proof += 1

        return proof

    """
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeros?
    :param last_proof: <int> Previous proof
    :param proof: <int> Current Proof
    :return <bool> True if correct, False if not.
    """
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"