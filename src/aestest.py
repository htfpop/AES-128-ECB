import tools
import AESEncrypt
import aesdecrypt
import os



def test_aes():
    #key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f] #Test vector FIPS 197
    #state = [[0x32, 0x88, 0x31, 0xe0], [0x43, 0x5a, 0x31, 0x37], [0xf6, 0x30, 0x98, 0x07], [0xa8, 0x8d, 0xa2, 0x34]]
    state = [0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff] #Test vector FIPS197

    aes_keys = AESEncrypt.key_expansion(key)

    round_key = AESEncrypt.extract_key(aes_keys[0])
    state = tools.xor_2d(state, round_key)

    for curr_round in range(1, 11, 1):

        print(f'[ENCRYPT]: round{curr_round}: Start of Round')
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[ENCRYPT]: round{curr_round}: After SubBytes')
        AESEncrypt.s_box_sub(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[ENCRYPT]: round{curr_round}: After ShiftRows')
        AESEncrypt.shift_rows(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        if curr_round != 10:
            print(f'[ENCRYPT]: round{curr_round}: After MixColumns')
            state = AESEncrypt.mix_cols(state)
            tools.debug_print_arr_2dhex_1line(state)
            print()

        print(f'[ENCRYPT]: round{curr_round}: Round key Value')
        round_key = AESEncrypt.extract_key(aes_keys[curr_round])
        state = tools.xor_2d(state, round_key)
        tools.debug_print_arr_2dhex_1line(round_key)
        print()

    print(f'AES Encrypt Complete')
    tools.debug_print_arr_2dhex_1line(state)
    print()

    print(f'[START] AES Decrypt')

    round_key = AESEncrypt.extract_key(aes_keys[10])

    print(f'[DECRYPT] round{0}: iinput')
    tools.debug_print_arr_2dhex_1line(state)
    print()

    print(f'[DECRYPT] round{0}: ik_sch')
    tools.debug_print_arr_2dhex_1line(round_key)
    print()

    state = tools.xor_2d(state, round_key)

    for inv_curr_round in range(9,-1,-1):

        print(f'[DECRYPT] round{10 - inv_curr_round}: istart')
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[DECRYPT] round{10 - inv_curr_round}: is_row')
        aesdecrypt.shift_rows_inv(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        print(f'[DECRYPT] round{10 - inv_curr_round}: is_box')
        aesdecrypt.s_box_inv_sub(state)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        round_key = AESEncrypt.extract_key(aes_keys[inv_curr_round])

        print(f'[DECRYPT] round{10 - inv_curr_round}: ik_sch')
        tools.debug_print_arr_2dhex_1line(round_key)
        print()

        print(f'[DECRYPT] round{10 - inv_curr_round}: ik_add')
        state = tools.xor_2d(state, round_key)
        tools.debug_print_arr_2dhex_1line(state)
        print()

        if inv_curr_round != 0:
            print(f'[DECRYPT] round{10 - inv_curr_round}: i_mix_cols')
            state = aesdecrypt.inv_mix_cols(state)
            tools.debug_print_arr_2dhex_1line(state)
            print()

    print(f'AES Decrypt Complete')
    tools.debug_print_arr_2dhex_1line(state)
    print()

if __name__ == '__main__':
    print("-------------------------------")
    print("CSCI-531 AES-128 Implementation")
    print("-------------------------------")
    #arr_key = tools.read_file("../input/key.txt")
    #tools.debug_print_arr_ascii(arr_key)

    #arr_pt = tools.read_file("../input/plaintext.txt")
    #tools.debug_print_arr_ascii(arr_pt)
    #testkey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

    key = os.urandom(16)
    tools.debug_print_arr_hex_1line(key)
    keyarr = AESEncrypt.key_expansion(key )

    tools.debug_print_arr_2dhex(keyarr)

    mykey = AESEncrypt.extract_key(keyarr[0])

    tools.debug_print_arr_2dhex(mykey)

    AESEncrypt.aes_main(key,key)
    #test_aes()
