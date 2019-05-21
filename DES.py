# Authors: Gilad Guralnik, ID: 205508955, Yoel Vaizman 204363659, Reuven Regev Farag 311496798

import binascii
from collections import deque
from string import ascii_lowercase


# S Boxes
S1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

S2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

S3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

S4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

S5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

S6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

S7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

S8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

# Initial permutation (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final permutation (IP−1)
IP_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

# Expansion function (E)
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Permutation (P)
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# Permuted choice 1 (PC-1)
PC_1 = [57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 27, 19, 11, 3,
        60, 52, 44, 36, 63, 55, 47, 39,
        31, 23, 15, 7, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 28, 20, 12, 4]

# Permuted choice 2 (PC-2)
PC_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# Left circular shift
LEFT_SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def string_to_binary(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def binary_to_string(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int_to_bytes(n).decode(encoding, errors)


def hex_to_binary(src_hex):
    src_hex = src_hex[2:]  # remove 0x
    res = ''
    for ch in src_hex:
        res += bin(int(str(ch), 16))[2:].zfill(4)

    return res


def binary_to_hex(src_bin):
    res = '0x'
    src_bin = [src_bin[i:i + 8] for i in range(0, len(src_bin), 8)]  # Divide the block into 8bit parts

    def func1(num):
        num = hex(int(num, 2))[2:]
        if len(num) == 1:
            num = "0"+num
            
        return num

    src_bin = list(map(lambda x: func1(x), src_bin))

    for x in src_bin:
        res += x
    return res
    

def int_to_bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def split_to_blocks(bin_text, block_size):
    return [list(bin_text[x:x + block_size]) for x in range(0, len(bin_text), block_size)]


def make_c_and_d(bin_key):
    c = []
    d = []
    for i in range(len(PC_1)//2):
        c.append(bin_key[PC_1[i]-1])

    for i in range(len(PC_1)//2, len(PC_1)):
        d.append(bin_key[PC_1[i]-1])

    return c, d


def shift_left(c, round_number):
    shifted = deque(c)
    shifted.rotate(-1 * LEFT_SHIFT[round_number])
    return list(shifted)


def mapping(source, matrix):
    res = []
    for i in range(len(matrix)):
        res.append(source[matrix[i]-1])
    return res


# Cut first half of string
def first_half(input):
    first = [0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(32):
        first[i] = input[i]
    return first


# Cut second half of string
def second_half(input):
    second = [0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(32):
        second[i] = input[i+32]
    return second


# Create selection table using E
def create_selection_table(secondHalf):
    output = [0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0]

    for i in range(48):
        output[i] = secondHalf[E[i]-1]

    return output


# xor input and key
def XOR48(input, key):
    output = [0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0]

    for i in range(48):
        if input[i] == key[i] and input[i] == '1':
            output[i] = '0'

        elif input[i] == key[i]:
            output[i] = '0'
        else:
            output[i] = '1'

    return output


# xor input and key
def XOR32(input, key):
    output = [0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0]

    for i in range(32):
        if input[i] == key[i] and input[i] == '1':
            output[i] = '0'

        elif input[i] == key[i]:
            output[i] = '0'
        else:
            output[i] = '1'

    return output


def sboxes(inputListBlock):
    sbox = [S1, S2, S3, S4, S5, S6, S7, S8]

    x = ''.join(inputListBlock)  # Convert the list to string
    input = [x[i:i + 6] for i in range(0, len(x), 6)]  # Divide the block into 6bit parts

    bin = lambda x: format(x, 'b').zfill(4)

    i = 0
    ans = ""
    for s in sbox:
        temp = input[i]
        row = int(temp[0] + temp[len(temp) - 1], 2)
        column = int(temp[1:len(temp) - 1], 2)
        ans = ans + bin(s[row][column])
        i = i + 1

    return list(ans)


def print_rows_by_column_number(src, rows_number):
    for i in range(1, len(src)+1):
        print(src[i - 1], end="")
        if i % rows_number == 0:
            print("")


def expand_to_64bit(block):
    result = []
    for i in range(64):
        result.append('0')
    for j in range(len(block)):
        result[j] = block[j]

    return result


def encrypt_des_one_block(block, keys, rounds_number):
    # USING ONLY ONE BLOCK
    bin_text_block = mapping(block, IP)

    left = first_half(bin_text_block)
    right = second_half(bin_text_block)

    # the f function
    def f(right, key):
        expanded_right = create_selection_table(right)
        expanded_right_after_xor = XOR48(key, expanded_right)
        right_after_sboxes = sboxes(expanded_right_after_xor)
        right_after_sboxes_and_p = mapping(right_after_sboxes, P)
        return right_after_sboxes_and_p

    # n rounds loop
    for i in range(rounds_number):
        old_left = left
        left = right
        right = XOR32(old_left, f(right, keys[i]))

    result = right + left
    result = mapping(result, IP_1)
    return ''.join(result)


def encrypt_des(block, key, rounds_number):
    bin_key = string_to_binary(key)
    c, d = make_c_and_d(bin_key)

    shifted_c = c
    shifted_d = d

    # keys array
    keys = []

    # keys creation
    for i in range(rounds_number):
        shifted_c = shift_left(shifted_c, i)
        shifted_d = shift_left(shifted_d, i)
        shifted_cd = shifted_c + shifted_d
        shifted_cd_after_pc_2 = mapping(shifted_cd, PC_2)
        keys.append(shifted_cd_after_pc_2)

    result = ""
    if len(block) != 64:
        print("EXPAND BLOCK (ENC)")
        block = expand_to_64bit(block)
    result += encrypt_des_one_block(block, keys, rounds_number)

    # convert to hex
    return binary_to_hex(result)


def decrypt_des_one_block(block, keys, rounds_number):
    # USING ONLY ONE BLOCK
    bin_text_block = mapping(block, IP)

    left = first_half(bin_text_block)
    right = second_half(bin_text_block)

    # the f function
    def f(right, key):
        expanded_right = create_selection_table(right)
        expanded_right_after_xor = XOR48(key, expanded_right)
        right_after_sboxes = sboxes(expanded_right_after_xor)
        right_after_sboxes_and_p = mapping(right_after_sboxes, P)
        return right_after_sboxes_and_p

    # n rounds loop
    for i in range(rounds_number):
        old_left = left
        left = right
        right = XOR32(old_left, f(right, keys[i]))  # reverse order keys

    result = right + left
    result = mapping(result, IP_1)
    return ''.join(result)


def decrypt_des(block, key, rounds_number):
    bin_key = string_to_binary(key)
    c, d = make_c_and_d(bin_key)

    shifted_c = c
    shifted_d = d

    # keys array
    keys = []

    # keys creation
    for i in range(rounds_number):
        shifted_c = shift_left(shifted_c, i)
        shifted_d = shift_left(shifted_d, i)
        shifted_cd = shifted_c + shifted_d
        shifted_cd_after_pc_2 = mapping(shifted_cd, PC_2)
        keys.append(shifted_cd_after_pc_2)
    
    keys.reverse()
    

    result = ""
    if len(block) != 64:
            print("EXPAND BLOCK (DEC)")
            block = expand_to_64bit(block)
    result += decrypt_des_one_block(block, keys, rounds_number)

    # convert from bin to hex
    return hex(int(result, 2))


def ascii_to_hex(str):
    res = ['0', 'x']
    for ch in str:
        ans = hex(ord(ch))[2:]
        res.append(ans)

    return ''.join(res)


def hex_to_ascii(hex_result):
    result = bin(int(hex_result, 16))[2:].zfill(8)
    try:
        result = binary_to_string(result)
    except Exception:
        print("Cannot convert " + hex_result + " hex to ascii!")
        exit(1)
    return result


def brute_force_des(plaintext, cypher, rounds_number):
    plaintext = ascii_to_hex(plaintext)
    for l1 in ascii_lowercase:
        for l2 in ascii_lowercase:
            for l3 in ascii_lowercase:
                for l4 in ascii_lowercase:
                    for l5 in ascii_lowercase:
                        for l6 in ascii_lowercase:
                            for l7 in ascii_lowercase:
                                for l8 in ascii_lowercase:
                                    guess = l1+l2+l3+l4+l5+l6+l7+l8
                                    print('guess:' + guess)
                                    if plaintext == decrypt_des(cypher, guess, rounds_number):
                                        print("KEY FOUND: " + guess)
                                        return guess


msg = "Hermione"
key = "d1D3!7$%"


# encrypt_des - receive string msg and string key and rounds number => returns hex encrypted msg
msg_encrypted_hex = encrypt_des(msg, key, 16)  # CHANGE ROUND NUMBER


# decrypt_des - receive hex string encrypted msg and string key and rounds number => returns hex decrypted msg
#msg_decrypted_hex = decrypt_des(msg_encrypted_hex, key, 16)  # pass hex number as string
# hex_to_ascii - tries to convert the ascii string to hex => if succeed prints it, else show error
# print("The originalText: " + ascii_to_hex(msg))
# print("The encryptedText: " + msg_encrypted_hex)
# print("The decryptedText: " + msg_decrypted_hex)
#
#
# print("The original plaintext: " + hex_to_ascii(msg_decrypted_hex))
