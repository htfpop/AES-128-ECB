import tools

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("-------------------------------")
    print("CSCI-531 AES-128 Implementation")
    print("-------------------------------")
    arr_key = tools.read_file("..\input\key.txt")
    tools.debug_print_arr_ascii(arr_key)

    arr_pt = tools.read_file("..\input\plaintext.txt")
    tools.debug_print_arr_ascii(arr_pt)

"""
    arr = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xf, 0x10, 0x11]
    arr2 = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xf, 0x10, 0x11]
    tools.debug_print_arr(arr)
    result = tools.xor(arr, arr2)
    tools.debug_print_arr(result)
"""


