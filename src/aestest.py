import tools
import AESEncrypt
import os

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

    plaintext = tools.read_file("../input/plaintext.txt")
    # testkey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    #tools.debug_print_plaintext_ascii(plaintext)

    padded_plaintext = iso_iec_7816_4_pad(plaintext)
    key = os.urandom(16)

    print(f'[aestest.py] AES Padded Plaintext (ASCII):')
    tools.debug_print_plaintext_ascii(padded_plaintext)
    print()

    print(f'[aestest.py] AES 16 Byte Key (HEX):')
    tools.debug_print_arr_hex_1line(key)
    print()

    AESEncrypt.aes_enc_main(padded_plaintext,key)
    #test_aes()
