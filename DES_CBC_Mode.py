from DES import *


def encrypt_des_cbc_mode(iv, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i+8]
        # first time convert iv from ascii to binary
        if i == 0:
            iv = string_to_binary(iv)
        # else, convert iv from hex to binary
        else:
            iv = hex_to_binary(iv)

        iv = list(iv)
        block = string_to_binary(block)
        block = list(block)  # convert to list
        if len(block) != 64:
            block = expand_to_64bit(block)
        block = XOR64(iv, block)

        iv = encrypt_des(block, key, rounds_number)[2:]
        result += iv
        i += 8
    return result


def decrypt_des_cbc_mode(iv, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        block = plaintext[i:i+16]
        temp = block
        # convert to binary and split plain text to 64 bit blocks and operate DES on any of them
        block = hex_to_binary(block)
        block = list(block)
        if len(block) != 64:
            block = expand_to_64bit(block)

        res = decrypt_des(block, key, rounds_number)[2:]
        res = list(hex_to_binary(res))
        if(i==0):
            iv = string_to_binary(iv)
        else:
            iv = hex_to_binary(iv)
        iv = list(iv)
        block = XOR64(iv, res)
        # flatten the list to string
        ans = ""
        for ch in block:
            ans += ch
        result += binary_to_hex(ans)[2:]
        iv = temp
        i += 16
    return result


iv = "mySecret"
msg = "Hermioneeee!!@$%RD$$$%55533"
msg = "HermioneHermion#$@#$#@$C@C@@@@CC@e"

key = "d1D3!7$%"
res = encrypt_des_cbc_mode(iv, msg, key, 16)
print("enc: " + res)
q1 = decrypt_des_cbc_mode(iv, res, key, 16)
q2 = hex_to_ascii(q1)
print("dec(bin): " + q1)
print("dec(ascii): " + q2)

