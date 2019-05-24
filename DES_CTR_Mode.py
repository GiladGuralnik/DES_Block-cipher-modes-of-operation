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
        block = XOR64(block, res)
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

        block = XOR64(block, res)

        # flatten the block to string
        ans = ""
        for ch in block:
            ans += ch

        result += binary_to_hex(ans)[2:]
        counter = original_counter + 1
        i += 16
    return result


# counter = 0
# msg = "HermioneHermion#$@#$#@$C@C@@@@CC@e"
#
# key = "d1D3!7$%"
# res = encrypt_des_ctr_mode(counter, msg, key, 16)
# print("enc: " + res)
# q1 = decrypt_des_ctr_mode(counter, res, key, 16)
# q2 = hex_to_ascii(q1)
# print("dec(bin): " + q1)
# print("dec(ascii): " + q2)

