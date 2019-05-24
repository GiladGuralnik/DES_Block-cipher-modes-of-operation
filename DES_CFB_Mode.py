from DES import *


def encrypt_des_cfb_mode(iv, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i+8]
        # plain text block to binary
        block = string_to_binary(block)
        block = list(block)  # convert to list
        if len(block) != 64:
            block = expand_to_64bit(block)

        # first time convert iv from ascii to binary
        if i == 0:
            iv = string_to_binary(iv)
        # else, convert iv from hex to binary
        else:
            iv = hex_to_binary(iv)

        iv = list(iv)
        if len(iv) != 64:
            iv = expand_to_64bit(iv)

        iv = encrypt_des(iv, key, rounds_number)[2:]
        iv = list(hex_to_binary(iv))

        block = XOR64(iv, block)

        # flatten block to string
        ans = ""
        for ch in block:
            ans += ch
        iv = binary_to_hex(ans)[2:]
        result += iv
        i += 8
    return result


def decrypt_des_cfb_mode(iv, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i + 16]
        origin_block = block
        # plain text block to binary
        block = hex_to_binary(block)
        block = list(block)  # convert to list
        if len(block) != 64:
            block = expand_to_64bit(block)

        # first time convert iv from ascii to binary
        if i == 0:
            iv = string_to_binary(iv)
        # else, convert iv from hex to binary
        else:
            iv = hex_to_binary(iv)

        iv = list(iv)
        if len(iv) != 64:
            iv = expand_to_64bit(iv)

        iv = encrypt_des(iv, key, rounds_number)[2:]
        iv = list(hex_to_binary(iv))

        res = XOR64(iv, block)

        # flatten block to string
        ans = ""
        for ch in res:
            ans += ch
        ans = binary_to_hex(ans)[2:]
        result += ans
        iv = origin_block
        i += 16
    return result



