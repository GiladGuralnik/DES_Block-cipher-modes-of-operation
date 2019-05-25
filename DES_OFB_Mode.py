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
        xor = XOR64(block, iv);

        # flatten the block
        ans = ""
        for ch in xor:
            ans += ch
        result += binary_to_hex(ans)[2:]
        i += 8
    return result

def decrypt_des_ofb_mode(iv, ciphertext, key, rounds_number):

    result = ""
    cypherIV=string_to_binary(iv)
    i = 0
    while i < len(ciphertext):
        block = ciphertext[i:i+16]
        block = "0x" + block
        block = hex_to_binary(block)

        cypherIV = list(cypherIV)  # convert to list
        cypherIV = encrypt_des(cypherIV, key, rounds_number)
        cypherIV = hex_to_binary(cypherIV)
        result +=binary_to_hex(XOR(64,block, cypherIV))[2:]
        i += 16

    return result


iv = "mySecret"
msg = "vaizmandsfdsfsdsdff@#%$#^!$@# yoel"
key = "yoelyoel"

res=encrypt_des_ofb_mode(iv,msg, key, 16)
print(res)
# res=decrypt_des_ofb_mode(iv,res, key, 16)
# res=hex_to_ascii(res)
# print("enc: " +res)
