import time

from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-71cdbece-955f-11ec-b249-a68c05a281ab'
pnconfig.publish_key = 'pub-c-28a7f24a-81df-470f-9a94-c8d9cb6c2a9c'
pnconfig.uuid = "b44a3c5f-41b3-4cff-9d7c-a307a0f63b60"

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(
            f'Channel: {message_object.channel}'
        )
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain
                )
                print('-- Successfully replce the local chain')
            except Exception as e:
                print(f'\n -- Did not replce chain: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n Set the new transaction in the transaction popl')


class PubSub():
    """
    Handles the publish/subscriber layer of the application.
    Provide communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish message onjects to the channel.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def brodcast_block(self, block):
        """
        Brodcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def brodcast_transaction(self, transaction):
        """
        Brodcast a transaction to all nodes.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()