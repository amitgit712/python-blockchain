import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA


def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA["hash"]


def test_add_block():
    blockchain = Blockchain()
    data = "test-data"
    blockchain.add_block(data)

    assert blockchain.chain[-1].data == data


@pytest.fixture
def blockchain_three_block():
    blockchain = Blockchain()

    for i in range(3):
        blockchain.add_block(i)
    return blockchain


def test_is_valid_chain(blockchain_three_block):
    Blockchain.is_valid_chain(blockchain_three_block.chain)


def test_is_valid_chain_bad_genesis(blockchain_three_block):
    blockchain_three_block.chain[0].hash = 'invalid_hash'

    with pytest.raises(Exception, match='genesis block must be valid'):
        Blockchain.is_valid_chain(blockchain_three_block.chain)


def test_replace_chain(blockchain_three_block):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_block.chain)

    assert blockchain.chain == blockchain_three_block.chain


def test_replace_chain_not_longer(blockchain_three_block):
    blockchain = Blockchain()

    with pytest.raises(Exception, match='The incoming chain must be longer'):
        blockchain_three_block.replace_chain(blockchain.chain)


def test_replace_chain_bad_chain(blockchain_three_block):
    blockchain = Blockchain()
    blockchain_three_block.chain[1].hash = 'bad_hash'

    with pytest.raises(Exception, match='The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_three_block.chain)
