from DES import *


def encrypt_des_cbc_mode(iv, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        # convert to binary
        block = plaintext[i:i+8]
        if i == 0:
            iv = string_to_binary(iv)
        else:
            iv = hex_to_binary(iv)

        iv = list(iv)
        print("TTT: "+str(len(iv)))
        block = string_to_binary(block)
        block = list(block)  # convert to list
        if len(block) != 64:
            print("EXPAND BLOCK (ENC)")
            block = expand_to_64bit(block)
        block = XOR64(iv, block)

        iv = encrypt_des(block, key, rounds_number)[2:]
        print("ASD")
        print(iv)
        result += iv
        i += 8
    return result


def decrypt_des_cbc_mode(iv, plaintext, key, rounds_number):
    result = ""
    i = 0
    while i < len(plaintext):
        block = plaintext[i:i+16]
        temp = block
        block = "0x" + block
        # convert to binary and split plain text to 64 bit blocks and operate DES on any of them
        block = hex_to_binary(block)
        block = list(block)
        if len(block) != 64:
            print("EXPAND BLOCK (ENC)")
            block = expand_to_64bit(block)
        result += decrypt_des(block, key, rounds_number)[2:]
        block = XOR64(block, block)
        i += 16
    return result

iv = "mySecret"
msg = "Hermioneeee!!@$%RD$$$%55533"
key = "d1D3!7$%"
res = encrypt_des_cbc_mode(iv, msg, key, 16)
print("enc: " + res)
# q = hex_to_ascii(decrypt_des_cbc_mode(iv, res,key,16))
# print("dec: " + q)

#gilad you like penis