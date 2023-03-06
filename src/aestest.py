import AESEncrypt
import os

"""
Function :   read_file
Parameters : path - File Path
Output :     None
Description: Reads file path to byte array
"""
def read_file(path):
    with open(path, "rb") as f_input:
        return f_input.read()

"""
Function :   debug_print_arr_hex_1line
Parameters : hex_array - 1D hexadecimal array
Output :     None
Description: Iterates through entire 1D array and prints to screen.
             used in aes_enc_main and aestest.py main
"""
def debug_print_arr_hex_1line(hex_array):
    for x in range(len(hex_array)):
        print(format(hex_array[x], '#02x'), end=' ')
    print()

"""
Function :   debug_print_plaintext_ascii
Parameters : input - array of hexadecimal 
Output :     None
Description: Iterates through entire array, converts hexadecimal to ASCII, then prints to screen
             Used in aes_dec_main and aestest.py main
"""
def debug_print_plaintext_ascii(input):
    for x in range(len(input)):
        print(f'{input[x]:c}', end='')
    print()

"""
Bytes is immutable, converting to byte array instead
"""
def iso_iec_7816_4_pad(pt):
    ret_pt = bytearray(pt)
    length = len(ret_pt)
    padding = 16 - (length % 16)

    if padding != 0:
        #Short first plaintext block
        if length <= 15:
            ret_pt.append(0x80)
            for i in range(16 - length -1):
                ret_pt.append(0x00)

        #subsequent short blocks
        else:
            ret_pt.append(0x80)
            for i in range(padding - 1):
                ret_pt.append(0x00)
    return ret_pt


if __name__ == '__main__':
    print("-----------------------------------")
    print("CSCI-531 AES-128 ECB Implementation")
    print("-----------------------------------")

    plaintext = read_file("../input/plaintext.txt")

    padded_plaintext = iso_iec_7816_4_pad(plaintext)
    key = os.urandom(16)

    print(f'[aestest.py] AES Padded Plaintext (ASCII):')
    debug_print_plaintext_ascii(padded_plaintext)
    print()

    print(f'[aestest.py] AES 16 Byte Key (HEX):')
    debug_print_arr_hex_1line(key)
    print()

    AESEncrypt.aes_enc_main(padded_plaintext,key)
