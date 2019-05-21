from DES import *


def encrypt_des_ecb_mode(plaintext, key, rounds_number):
    result = "0x"
    i = 0
    while i < len(plaintext):
        block = plaintext[i:i+8]
        result += encrypt_des(block, key, rounds_number)[2:]
        i += 8
    return result


def decrypt_des_ecb_mode(plaintext, key, rounds_number):
    plaintext = plaintext[2:]
    result = "0x"
    i = 0
    while i < len(plaintext)-2:
        block = plaintext[i:i+16]
        block = "0x" + block
        result += decrypt_des(block, key, rounds_number)[2:]
        i += 16
    return result


msg = "Hermionee"
key = "d1D3!7$%"
res = encrypt_des_ecb_mode(msg, key, 16)
print("enc: " + res)
q = hex_to_ascii(decrypt_des_ecb_mode(res,key,16))
print("dec: " + q)