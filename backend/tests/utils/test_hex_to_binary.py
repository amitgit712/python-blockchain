from backend.utils.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    org_num = 789
    hex_num = hex(org_num)[2:]
    binary_num = hex_to_binary(hex_num)

    assert int(binary_num, 2) == org_num
