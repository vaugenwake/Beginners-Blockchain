import asyncio
import json
import math
import random
from hashlib import sha256
from time import time
import structlog

"""
* Main class holding and building up the block chain
"""

logger = structlog.getLogger("blockchain")


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.target = "0000"

        # Create the genesis block
        logger.info("Creating genesis block")
        self.chain.append(self.new_block())

    """
    Create a new block from pending transactions and return a new block
    to be added to the chain
    """

    def new_block(self):
        block = self.create_block(
            height=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.last_block["hash"] if self.last_block else None,
            nonce=format(random.getrandbits(64), "x"),
            timestamp=time()
        )

        # Reset the list of pending transactions
        self.pending_transactions = []
        return block

    """
    Create a new block and calculate its hash
    :param <int> height
    :param <Dict> transactions
    :param <str> previous_hash
    :param <int> nonce
    :param <str> mining target
    :param <Time> timestamp
    :return block
    """
    @staticmethod
    def create_block(height, transactions, previous_hash, nonce, timestamp=None):
        block = {
            "height": height,
            "transactions": transactions,
            "previous_hash": previous_hash,
            "nonce": nonce,
            "timestamp": timestamp or time()
        }

        # Get the has of the new block
        # Ensure block is always in the same order for accurate output
        block_string = json.dumps(block, sort_keys=True).encode()
        block["hash"] = sha256(block_string).hexdigest()
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    """
    Get the last block in the chain
    :return block
    """
    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    """
    Check if the blocks hash is less than the target
    :return bool
    """

    def valid_block(self, block):
        return block["hash"].startswith("0000")

    """
    Add a block to the chain
    :return void
    """

    def add_block(self, block):
        self.chain.append(block)

    """
    Add a new transaction
    """

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "recipient": recipient,
            "sender": sender,
            "amount": amount
        })
        logger.info("New block added")

    """
    Recalculate the number to get below to mine the block
    :param <int> block_index
    :return int
    """

    def recalculate_target(self, block_index):
        if block_index % 10 == 0:
            # Expected time span of 10 blocks
            expected_timespan = 10 * 10

            # calculate the actual time span
            actual_timespan = self.chain[-1]["timestamp"] - \
                self.chain[-10]["timestamp"]

            # Figure out what the offset is
            ratio = actual_timespan / expected_timespan

            # Adjust the ratio to not to be too extream
            ratio = max(0.25, ratio)
            ratio = min(4.00, ratio)

            # Calculate the new target
            new_target = int(self.target, 16) * ratio

            self.target = format(math.floor(new_target), "x").zfill(64)
            logger.info(f"Calculated new mining target: {self.target}")

        return self.target

    """
    Get blocks after 
    """
    async def get_blocks_after_timestamp(self, timestamp):
        for index, block in enumerate(self.chain):
            if timestamp < block["timestamp"]:
                return self.chain[index:]

    """
    Mine a new block to be added into the chain
    :return void
    """

    async def mine_new_block(self):
        self.recalculate_target(self.last_block["height"] + 1)

        while True:
            new_block = self.new_block()

            if self.valid_block(new_block):
                break

            await asyncio.sleep(0)

        self.chain.append(new_block)
        logger.info("Found new block: ")
        logger.info(new_block)
        logger.info("New chain")
        logger.info(self.chain)
