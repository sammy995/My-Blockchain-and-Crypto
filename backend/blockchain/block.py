import time
from backend.Util.crypto_hash import crypto_hash
from backend.Util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA ={
    'timestamp' : 1,
    'last_hash' :'genesis_last_hash',
    'hash' : 'genesis_hash',
    'data' :[],
    'difficulty' :3,
    'nonce' : 'genesis_nonce'
}


class Block:
    """
    Block is unit of storage. Stores transactions
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return( 
            'Block('
            f'timestamp : {self.timestamp}, '
            f'last_hash : {self.last_hash}, '
            f'hash : {self.hash}, '
            f'data : {self.data}, '
            f'difficulty : {self.difficulty}, '
            f'nonce : {self.nonce}'
        )

    def to_json(self):
        """
        Serialize the block into a dict
        """
        return self.__dict__


    #Special function for comparing two objects using their dict
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
     Mines a block based on given inputs, until a block hash meets POW difficulty
     """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty =Block.adjust_difficulty(last_block, timestamp)
        nonce= 0
        hash = crypto_hash(timestamp,last_hash,data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' *difficulty:
            nonce += 1
           # n_timestamp = time.time_ns()
            hash = crypto_hash(timestamp,last_hash,data, difficulty, nonce)
            #Sending updated timestamp for hash calculation but sending orignal timestamp while returning the block.
        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        Create Genesis block for blockchain
        """
        # return Block(
        #    timestamp = GENESIS_DATA['timestamp'],
        #     last_hash = GENESIS_DATA['last_hash'],
        #     hash = GENESIS_DATA['hash'],
        #     data = GENESIS_DATA['data']
        # )
        return Block(**GENESIS_DATA) # same as above commented lines


    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation into a block
        """
        return Block(**block_json) 

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to MINE_RATE.
        Increases difficulty for quickly mined blocks and decreases for slowly mined blocks.
        """
        if(new_timestamp - last_block.timestamp) < MINE_RATE:
            #print(f"newTime: {new_timestamp}, last_time :{last_block.timestamp}, diff :{new_timestamp - last_block.timestamp}, MINERATE :{MINE_RATE}, di :{last_block.difficulty + 1}")
            return last_block.difficulty + 1
        if (last_block.difficulty - 1 >0): 
        #((new_timestamp - last_block.timestamp) >= MINE_RATE) & :
           #print(f"newTime: {new_timestamp}, last_time :{last_block.timestamp}, diff :{new_timestamp - last_block.timestamp} , MINERATE :{MINE_RATE} , di :{last_block.difficulty - 1}")
            return last_block.difficulty - 1
        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate a block to ensure it hasn't been tampered.
            - the block must have proper last_hash reference
            - the block must meet POW requirement
            - the difficulty must only adjust by 1
            - the block hash must be a valid combination of block fields 

        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct.')
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The Proof of requirement was not met.')
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('Block difficulty must be adjusted by 1 only.')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )
        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')



def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
   # bad_block.last_hash = 'evil hash'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block :{e}')


if __name__ == '__main__': 
    main() # used to execute only if main is called   
"""
python3 blockchain.py
Output:
Block Data foo
blockchain.py __name__ : block <- module
Blockchain [Block Data 1, Block Data 2]
blockchain.py __name__ : __main__ <-module
"""