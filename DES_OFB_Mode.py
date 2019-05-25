from DES import *


def encrypt_des_ofb_mode(iv, plaintext, key, rounds_number):
    result = ""
    iv = list(string_to_binary(iv))
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i+8]
        block = string_to_binary(block)
        if len(block) != 64:
            print("EXPAND BLOCK (ENC)")
            block = expand_to_64bit(block)

        iv = encrypt_des(iv, key, rounds_number)[2:]
        iv = list(hex_to_binary(iv))
        xor = XOR(block, iv)

        # flatten the block
        ans = ""
        for ch in xor:
            ans += ch
        result += binary_to_hex(ans)[2:]
        i += 8
    return result


def decrypt_des_ofb_mode(iv, ciphertext, key, rounds_number):
    result = ""
    iv = list(string_to_binary(iv))
    i = 0
    while i < len(ciphertext):
        block = ciphertext[i:i+16]
        block = hex_to_binary(block)

        iv = encrypt_des(iv, key, rounds_number)[2:]
        iv = hex_to_binary(iv)
        xor = XOR(block, iv)

        # flatten the block
        ans = ""
        for ch in xor:
            ans += ch
        result += binary_to_hex(ans)[2:]
        i += 16
    return result
