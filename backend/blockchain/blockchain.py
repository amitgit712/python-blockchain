from backend.blockchain.block import Block


class Blockchain:
    """
    BlockChain: a public ledger transactions.
    Implemented as a list of blocks - data sets of
    tramsactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f"Blockchain {self.chain}"

    def replace_chain(self, chain):
        """
        Replace the local chain with incomming one if the
        following rules applies:
            - The incomming chain must be longer than the local one.
            - The incomming chain is formatted properly.
        """
        if len(chain) <= len(self.chain):
            raise Exception(
                'Cannot replace. The incoming chain must be longer.'
            )
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(
                f'Cannot replace. The incoming chain is invalid: {e}'
            )

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize list of serialized blocks into a blockchain instance.
        The result will contain a chain list of blockchian
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(
            lambda block_json: Block.from_json(block_json),
            chain_json
        ))
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validet the incomming chain.
        Enforce the following rules of the blockchin:
            - The chain must start with genesis block.
            -  blocks must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)


def main():
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")
    blockchain.add_block("three")

    print(blockchain)
    print(f"blockchain.py __name___: {__name__}")


if __name__ == "__main__":
    main()
