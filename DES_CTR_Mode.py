from DES import *


def encrypt_des_ctr_mode(counter, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i+8]
        original_counter = counter
        counter = string_to_binary(str(counter))
        counter = list(counter)
        if len(counter) != 64:
            counter = expand_to_64bit(counter)

        block = string_to_binary(block)
        block = list(block)  # convert to list
        if len(block) != 64:
            block = expand_to_64bit(block)

        res = encrypt_des(counter, key, rounds_number)[2:]

        res = list(hex_to_binary(res))
        block = XOR(block, res)
        # flatten the block to string
        ans = ""
        for ch in block:
            ans += ch

        result += binary_to_hex(ans)[2:]
        counter = original_counter+1
        i += 8
    return result


def decrypt_des_ctr_mode(counter, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i + 16]
        original_counter = counter
        counter = string_to_binary(str(counter))
        counter = list(counter)
        if len(counter) != 64:
            counter = expand_to_64bit(counter)

        block = hex_to_binary(block)
        block = list(block)  # convert to list
        if len(block) != 64:
            block = expand_to_64bit(block)

        res = encrypt_des(counter, key, rounds_number)[2:]

        res = list(hex_to_binary(res))

        block = XOR(block, res)

        # flatten the block to string
        ans = ""
        for ch in block:
            ans += ch

        result += binary_to_hex(ans)[2:]
        counter = original_counter + 1
        i += 16
    return result

