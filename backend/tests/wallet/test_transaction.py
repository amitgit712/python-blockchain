import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 9000)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)

    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet, 'new_recipient', 9000)


def test_transaction_update():
    sender_wallet = Wallet()
    firs_recipient = 'first_recipient'
    first_amount = 50
    transaction = Transaction(sender_wallet, firs_recipient, first_amount)

    next_recipient = 'next_recipient'
    next_amount = 75

    transaction.update(sender_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )
    amount = 25
    transaction.update(sender_wallet, firs_recipient, amount)
    assert transaction.output[firs_recipient] == \
        first_amount + amount

    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount - amount

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))


def test_valide_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 9000

    with pytest.raises(Exception, match='Invalid transaction'):
        Transaction.is_valid_transaction(transaction)


def test_valide_transaction_with_invalid_signature():
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.is_valid_transaction(transaction)
