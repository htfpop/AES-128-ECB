# Constants
AES_KEY_SIZE = 16
PT_BLOCK_SIZE = 16
AES_PT_PADDING = 0x00

# Error Codes
INVALID_KEY_SIZE = 0xDEADDEAD


def debug_print_arr_hex(hex_array):
    for x in range(len(hex_array)):
        if x % 4 == 0 and x != 0:
            print("\r\n")
        print(f'0x{hex_array[x]:02x}', end=' ')
    print()

def debug_print_arr_2dhex(hex_array):
    for row in hex_array:
        for col in row:
            print(f'{col:#04x}', end=' ')
        print()

def debug_print_arr_ascii(hex_array):
    for x in range(len(hex_array)):
        if x % 8 == 0 and x != 0:
            print("\r\n")
        print(f'{hex_array[x]:c}', end=' ')
    print()


def xor(arr1, arr2):
    return [a ^ b for a, b in zip(arr1, arr2)]


def add(arr1, arr2):
    return [a + b for a, b in zip(arr1, arr2)]


def read_file(path):
    with open(path, "rb") as f_input:
        return f_input.read()


def read_AES_key(path):
    with open(path, "rt") as AES_Key:
        hex_arr = bytearray.fromhex(AES_Key.read())
        return hex_arr

"""
        if len(key) != AES_KEY_SIZE:
            print(f'[ERROR]: Input AES key is {len(key)} bytes. Should be {AES_KEY_SIZE} bytes. Exiting now...')
            exit(INVALID_KEY_SIZE)
        else:
            return key
"""


def read_plaintext(path):
    with open(path, "rb") as pt:
        pt = pt.read()
        if len(pt) % PT_BLOCK_SIZE != 0:
            print(f'[NOTICE]: Plaintext size is {len(pt)}, padding to nearest multiple of {PT_BLOCK_SIZE}')
            for i in range(1, len(pt) % PT_BLOCK_SIZE):
                pt += AES_PT_PADDING
        return pt


def bin_test(hexnum):
    hexnum += 0x1
    print(f'Hex + 1 0x{hexnum:02x}')

def compare_2d(arr1, arr2):
    status = 0
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            if arr1[i][j] != arr2[i][j]:
              status = -1

    return status

