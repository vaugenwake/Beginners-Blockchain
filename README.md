# Build a blockchain

Learning about blockchains and how they working by building a basic blockchain

### TODO:
* Implement validation and consensus
* Add a `merkle tree` hash for each block to validate transactions in each block are complete
* Add a digital wallet to allow peers to transact with key pairs and addresses
* Implement peer-to-peer communcation to broadcast new transactions and mine blocks

### A Block:
The data in each block
```
- #Magic number -> Static value to identify the type of block
- Blocksize -> Total size of the block
- Block header ->
  - Version -> Version of block scheme present
  - Prev hash -> Hash of the prev block header
  - Merkle Root -> Merkle hash of transactions
  - Timestamp -> Time block was created
  - target -> Difficulty of the block
  - Nonce -> The key to be added that when hashed will result in the blocks hash
- Header Hash -> Hash of the header data
- Transaction Counter -> Number of transactions in block
- Transactions[] -> A list of all the transactions in the block
```

#### Mining a new block:
`sha256(merkle_root + prev_hash + nonce) == target`
To mine a new block we will take the merkle root of the transactions and append the previous blocks hash + the nonce. We will then evaluate the hash and see if we have reached the target, if not we will increament the nonce and hash again until we find the target hash.

This is also know as a proof-of-work, as miners will compete to be the first to solve the hash to earn a reward in the form of a transaction fee. Only the origional solver of the hash will recieve the reward.
