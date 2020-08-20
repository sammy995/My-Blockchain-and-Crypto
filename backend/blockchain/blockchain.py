from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.Util.crypto_hash import crypto_hash
from backend.config import MINING_REWARD_INPUT
""" Evaluates entire file before going into code below
    To control it 
"""

class Blockchain:
    """"Blockchain is distributed ledger of transactions
        Implemented as list
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def __repr__(self):
        return f"Blockchain {self.chain}"

    def add_block(self,data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following applies:
          - The incoming chain is longer than the local one.
          - The incoming chain is formatted properly.
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer.')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks
        """
        # serialized_chain = []
        # for block in self.chain:
        #     serialized_chain.append(block.to_json())
        # return serialized_chain
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of json representation into a blockchain instance
        Result will have chain list of Block instance
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json :Block.from_json(block_json), chain_json))

        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate incoming chain 
        - Chain must start with genesis block
        - blocks must be formatted correctly. 
        """
        if chain[0] != Block.genesis():
            raise Exception('The Genesis block must be valid')

        for i in range(1,len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block,block)

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce rules of a chain composed of blocks of transaction
         - Each transaction must appear only once in the chain
         - There can only be one mining reward per block
         - Each transaction must be valid.
        """
        transaction_ids =set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)


                if transaction.id in transaction_ids:
                    raise Exception(f' Transaction : {transaction.id} is not unique')
                
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f'There can be only one mining reward per block.'\
                            f'\nCheck the block with hash " {block.hash}')
                    has_mining_reward = True
                else:

                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]

                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain, 
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has an invalid' \
                            'input amount')

                Transaction.is_valid_transaction(transaction)


if __name__ == '__main__':   
    blockchain = Blockchain()
    blockchain.add_block('1')
    blockchain.add_block('2')
    print(blockchain)
    print(f'blockchain.py __name__ : {__name__}') #Takes name of module it is executing - Used for debugging

"""
python3 blockchain.py
Output:
Block Data foo
blockchain.py __name__ : block <- module
Blockchain [Block Data 1, Block Data 2]
blockchain.py __name__ : __main__ <-module
"""