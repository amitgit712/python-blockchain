from backend.utils.crypto_hash import crypto_hash


def test_crypto_hash():
    """
    Test for crypto hash it should create the same
    hash with args for different data types in any order
    """
    assert crypto_hash(1, [2], "three") == crypto_hash("three", 1, [2])
    assert (
        crypto_hash("three")
        == "097a4dfb7f430ff3e44aa2399549a038c1f29465540d1e18701e8b5cd3fd2ccb"
    )
