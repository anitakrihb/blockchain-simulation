import hashlib
import time
import json

# Block class represents an individual block in the blockchain
class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index  # Block number
        self.timestamp = time.time()  # Time of creation
        self.transactions = transactions  # List of transactions (dummy data)
        self.previous_hash = previous_hash  # Hash of the previous block
        self.nonce = nonce  # Nonce for proof-of-work
        self.hash = self.calculate_hash()  # Current block hash

    def calculate_hash(self):
        """Generates SHA-256 hash of the block's contents."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Performs simple Proof-of-Work by finding a hash with a specific number of leading zeros."""
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

# Blockchain class to manage the chain of blocks
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = [self.create_genesis_block()]  # Initialize with Genesis block
        self.difficulty = difficulty  # Difficulty level for mining

    def create_genesis_block(self):
        """Creates the first block in the blockchain, known as the Genesis Block."""
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        """Returns the most recent block in the chain."""
        return self.chain[-1]

    def add_block(self, transactions):
        """Adds a new block to the blockchain after mining."""
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), transactions, previous_block.hash)
        new_block.mine_block(self.difficulty)  # Mining the block
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Checks the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash is still valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the block is properly linked to the previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def tamper_block(self, index, new_transactions):
        """Simulates data tampering by modifying a block's transactions."""
        if 0 < index < len(self.chain):  # Ensure the Genesis block is not modified
            self.chain[index].transactions = new_transactions
            self.chain[index].hash = self.chain[index].calculate_hash()

    def display_chain(self):
        """Prints out all the blocks in the blockchain."""
        for block in self.chain:
            print("\n---------------------------")
            print(f"Block #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Current Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")

# Running the blockchain simulation
if __name__ == "__main__":
    my_blockchain = Blockchain(difficulty=3)

    # Adding new blocks
    my_blockchain.add_block("Alice pays Bob 10 BTC")
    my_blockchain.add_block("Bob pays Charlie 5 BTC")

    print("\nInitial Blockchain:")
    my_blockchain.display_chain()

    # Validating the blockchain before tampering
    print("\nBlockchain Valid:", my_blockchain.is_chain_valid())

    # Tampering with the blockchain to simulate fraud
    my_blockchain.tamper_block(1, "Alice pays Bob 100 BTC")

    print("\nTampered Blockchain:")
    my_blockchain.display_chain()

    # Checking blockchain validity after tampering
    print("\nBlockchain Valid After Tampering:", my_blockchain.is_chain_valid())
