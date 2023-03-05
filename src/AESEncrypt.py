import tools
import copy

mix_col_matrix = [ [0x02, 0x03, 0x01, 0x01],
                   [0x01, 0x02, 0x03, 0x01],
                   [0x01, 0x01, 0x02, 0x03],
                   [0x03, 0x01, 0x01, 0x02] ]

inv_mix_col_matrix = [ [0x0E, 0x0B, 0x0D, 0x09],
                       [0x09, 0x0E, 0x0B, 0x0D],
                       [0x0D, 0x09, 0x0E, 0x0B],
                       [0x0B, 0x0D, 0x09, 0x0E] ]

r_const = [0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,0x40000000,0x80000000,0x1B000000,0x36000000]

s_box = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

s_box_inv = [[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
            [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
            [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
            [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
            [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
            [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
            [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
            [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
            [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
            [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
            [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
            [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
            [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
            [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
            [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]]


def s_box_sub(state):

    for i, row in enumerate(state):
        for j, col in enumerate(row):
            ms_nibble = (state[i][j] & 0xF0) >> 4
            ls_nibble = (state[i][j] & 0x0F)
            state[i][j] = s_box[ms_nibble][ls_nibble]

    return state

def sub_word(input_word):
    byte_arr = input_word.to_bytes(4, 'big')
    ret_word = [0,0,0,0]
    for i, byte in enumerate(byte_arr):
        ms_nibble = (byte & 0xF0) >> 4
        ls_nibble = (byte & 0x0F)
        ret_word[i] = s_box[ms_nibble][ls_nibble]

    return int.from_bytes(ret_word, 'big')



def mix_cols(state):
    temp = [[0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00]]

    for i, row in enumerate(temp):
        for j, col in enumerate(row):
            curr_col = [state[0][j], state[1][j], state[2][j], state[3][j]]
            temp[i][j] = mix_columns_transform(i, curr_col)

    return temp

def inv_mix_cols(state):
    temp = [[0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00]]

    for i, row in enumerate(temp):
        for j, col in enumerate(row):
            curr_col = [state[0][j], state[1][j], state[2][j], state[3][j]]
            temp[i][j] = inv_mix_columns_transform(i, curr_col)

    return temp

def inv_mix_columns_transform(I_row, S_Col):
    arr = [0,0,0,0]

    for i in range(len(inv_mix_col_matrix[I_row])):
        element = inv_mix_col_matrix[I_row][i]
        temp = 0x00

        #decimal value of 9: ((((x * 2) * 2) * 2) + x)
        if element == 0x09:
            #(x * 2)
            temp = S_Col[i] & 0xFF
            arr[i] = (S_Col[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((x * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((x * 2) * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((((x * 2) * 2) * 2) + x)
            arr[i] ^= S_Col[i]

            arr[i] = arr[i] & 0xFF

        # decimal value of 11: (((((x * 2) * 2) + x) * 2) + x)
        elif element == 0x0B:
            #(x * 2)
            temp = S_Col[i]
            arr[i] = (S_Col[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((x * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((x * 2) * 2) + x)
            arr[i] ^= S_Col[i]

            #((((x * 2) * 2) + x) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((((x * 2) * 2) + x) * 2) + x)
            arr[i] ^= S_Col[i]

            arr[i] = arr[i] & 0xFF

        # decimal value of 13: (((((x × 2) + x) × 2) × 2) + x)
        elif element == 0x0D:
            #(x * 2)
            temp = S_Col[i]
            arr[i] = (S_Col[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((x * 2) + x)
            arr[i] ^= S_Col[i]

            #((((x * 2) + x) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((((x * 2) + x) * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((((x * 2) + x) * 2) * 2) + x)
            arr[i] ^= S_Col[i]

            arr[i] = arr[i] & 0xFF

        # decimal value of 14: (((((x × 2) + x) × 2) + x) * 2)
        elif element == 0x0E:
            #(x × 2)
            arr[i] ^= (S_Col[i] << 1)
            if (S_Col[i] & 0xFF) >= 0x80: arr[i] ^= 0x1B

            #((x × 2) + x)
            arr[i] ^= S_Col[i]

            #(((x × 2) + x) × 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((((x × 2) + x) × 2) + x)
            arr[i] ^= S_Col[i]

            #(((((x × 2) + x) × 2) + x) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            arr[i] = arr[i] & 0xFF

    return (arr[0] ^ arr[1] ^ arr[2] ^ arr[3]) & 0xFF

def mix_columns_transform(I_row, S_Col):
    temp = 0x00

    for i in range(len(mix_col_matrix[I_row])):
        element = mix_col_matrix[I_row][i]

        if element == 0x02:
            temp ^= (S_Col[i] << 1)
            if S_Col[i] >= 0x80:
                temp ^= 0x1B

        elif element == 0x03:
            temp ^= S_Col[i] ^ (S_Col[i] << 1)

            if S_Col[i] >= 0x80:
                temp ^= 0x1B

        else:
            temp ^= S_Col[i]

    return temp & 0xFF

def inv_mix_cols_test():
    print(f'[START] Inv Columns Test:')

    before0 = [[0xd4, 0xe0, 0xb8, 0x1e], [0xbf, 0xb4, 0x41, 0x27], [0x5d, 0x52, 0x11, 0x98], [0x30, 0xae, 0xf1, 0xe5]]
    state = mix_cols(before0)
    state = inv_mix_cols(state)
    tools.compare_2d(state, before0, 0)
    tools.debug_print_arr_2dhex(state)
    print()

    before1 = [[0x49, 0x45, 0x7f, 0x77], [0xdb, 0x39, 0x02, 0xde], [0x87, 0x53, 0xd2, 0x96], [0x3b, 0x89, 0xf1, 0x1a]]
    state = mix_cols(before1)
    state = inv_mix_cols(state)
    tools.compare_2d(state, before1, 1)
    tools.debug_print_arr_2dhex(state)
    print()

    before2 = [[0xac, 0xef, 0x13, 0x45], [0xc1, 0xb5, 0x23, 0x73], [0xd6, 0x5a, 0xcf, 0x11], [0xb8, 0x7b, 0xdf, 0xb5]]
    state = mix_cols(before2)
    state = inv_mix_cols(state)
    tools.compare_2d(state, before2, 2)
    tools.debug_print_arr_2dhex(state)
    print()

    before3 = [[0x52, 0x85, 0xe3, 0xf6], [0xa4, 0x11, 0xcf, 0x50], [0xc8, 0x6a, 0x2f, 0x5e], [0x94, 0x28, 0xd7, 0x07]]
    state = mix_cols(before3)
    state = inv_mix_cols(state)
    tools.compare_2d(state, before3, 3)
    tools.debug_print_arr_2dhex(state)
    print()

    before4 = [[0xe1, 0xe8, 0x35, 0x97], [0xfb, 0xc8, 0x6c, 0x4f], [0x96, 0xae, 0xd2, 0xfb], [0x7c, 0x9b, 0xba, 0x53]]
    state = mix_cols(before4)
    state = inv_mix_cols(state)
    tools.compare_2d(state, before4, 4)
    tools.debug_print_arr_2dhex(state)
    print()

    before5 = [[0xa1, 0x78, 0x10, 0x4c], [0x4f, 0xe8, 0xd5, 0x63], [0x3d, 0x03, 0xa8, 0x29], [0xfe, 0xfc, 0xdf, 0x23]]
    state = mix_cols(before5)
    state = inv_mix_cols(state)
    tools.compare_2d(state, before5, 5)
    tools.debug_print_arr_2dhex(state)
    print()

    print(f'[END] Inv Mix Columns Test:\r\n')


def mix_cols_test():

    print(f'[START] Mix Columns Test:')
    before0 = [[0xd4, 0xe0, 0xb8, 0x1e], [0xbf, 0xb4, 0x41, 0x27], [0x5d, 0x52, 0x11, 0x98], [0x30, 0xae, 0xf1, 0xe5]]
    state = mix_cols(before0)
    KAT0 = [[0x04, 0xe0, 0x48, 0x28], [0x66, 0xcb, 0xf8, 0x06], [0x81, 0x19, 0xd3, 0x26], [0xe5, 0x9a, 0x7a, 0x4c]]
    tools.compare_2d(state, KAT0, 0)



    before1 = [[0x49, 0x45, 0x7f, 0x77], [0xdb, 0x39, 0x02, 0xde], [0x87, 0x53, 0xd2, 0x96], [0x3b, 0x89, 0xf1, 0x1a]]
    state = mix_cols(before1)
    KAT1 = [0x58, 0x1b, 0xdb, 0x1b], [0x4d, 0x4b, 0xe7, 0x6b], [0xca, 0x5a, 0xca, 0xb0], [0xf1, 0xac, 0xa8, 0xe5]
    tools.compare_2d(state, KAT1, 1)


    before2 = [[0xac, 0xef, 0x13, 0x45], [0xc1, 0xb5, 0x23, 0x73], [0xd6, 0x5a, 0xcf, 0x11], [0xb8, 0x7b, 0xdf, 0xb5]]
    state = mix_cols(before2)
    KAT2 = [0x75, 0x20, 0x53, 0xbb], [0xec, 0x0b, 0xc0, 0x25], [0x09, 0x63, 0xcf, 0xd0], [0x93, 0x33, 0x7c, 0xdc]
    tools.compare_2d(state, KAT2, 2)


    before3 = [[0x52, 0x85, 0xe3, 0xf6], [0xa4, 0x11, 0xcf, 0x50], [0xc8, 0x6a, 0x2f, 0x5e], [0x94, 0x28, 0xd7, 0x07]]
    state = mix_cols(before3)
    KAT3 = [0x0f, 0x60, 0x6f, 0x5e], [0xd6, 0x31, 0xc0, 0xb3], [0xda, 0x38, 0x10, 0x13], [0xa9, 0xbf, 0x6b, 0x01]
    tools.compare_2d(state, KAT3, 3)


    before4 = [[0xe1, 0xe8, 0x35, 0x97], [0xfb, 0xc8, 0x6c, 0x4f], [0x96, 0xae, 0xd2, 0xfb], [0x7c, 0x9b, 0xba, 0x53]]
    state = mix_cols(before4)
    KAT4 = [0x25, 0xbd, 0xb6, 0x4c], [0xd1, 0x11, 0x3a, 0x4c], [0xa9, 0xd1, 0x33, 0xc0], [0xad, 0x68, 0x8e, 0xb0]
    tools.compare_2d(state, KAT4, 4)


    before5 = [[0xa1, 0x78, 0x10, 0x4c], [0x4f, 0xe8, 0xd5, 0x63], [0x3d, 0x03, 0xa8, 0x29], [0xfe, 0xfc, 0xdf, 0x23]]
    state = mix_cols(before5)
    KAT5 = [[0x4b, 0x2c, 0x33, 0x37], [0x86, 0x4a, 0x9d, 0xd2], [0x8d, 0x89, 0xf4, 0x18], [0x6d, 0x80, 0xe8, 0xd8]]
    tools.compare_2d(state, KAT5, 5)

    print(f'[END] Mix Columns Test:\r\n')


def sub_bytes_test():
    print(f'[START] Sub bytes Test')
    before0 = [[0x19, 0xa0, 0x9a, 0xe9], [0x3d, 0xf4, 0xc6, 0xf8], [0xe3, 0xe2, 0x8d, 0x48], [0xbe, 0x2b, 0x2a, 0x08]]
    state = s_box_sub(before0)
    KAT0 = [[0xd4, 0xe0, 0xb8, 0x1e], [0x27, 0xbf, 0xb4, 0x41], [0x11, 0x98, 0x5d, 0x52], [0xae, 0xf1, 0xe5, 0x30]]
    tools.compare_2d(state, KAT0, 0)

    before1 = [[0xa4, 0x68, 0x6b, 0x02], [0x9c, 0x9f, 0x5b, 0x6a], [0x7f, 0x35, 0xea, 0x50], [0xf2, 0x2b, 0x43, 0x49]]
    state = s_box_sub(before1)
    KAT1 = [[0x49, 0x45, 0x7f, 0x77], [0xde, 0xdb, 0x39, 0x02], [0xd2, 0x96, 0x87, 0x53], [0x89, 0xf1, 0x1a, 0x3b]]
    tools.compare_2d(state, KAT1, 1)

    before2 = [[0xaa, 0x61, 0x82, 0x68], [0x8f, 0xdd, 0xd2, 0x32], [0x5f, 0xe3, 0x4a, 0x46], [0x03, 0xef, 0xd2, 0x9a]]
    state = s_box_sub(before2)
    KAT2 = [[0xac, 0xef, 0x13, 0x45], [0x73, 0xc1, 0xb5, 0x23], [0xcf, 0x11, 0xd6, 0x5a], [0x7b, 0xdf, 0xb5, 0xb8]]
    tools.compare_2d(state, KAT2, 2)

    before3 = [[0x48, 0x67, 0x4d, 0xd6], [0x6c, 0x1d, 0xe3, 0x5f], [0x4e, 0x9d, 0xb1, 0x58], [0xee, 0x0d, 0x38, 0xe7]]
    state = s_box_sub(before3)
    KAT3 = [[0x52, 0x85, 0xe3, 0xf6], [0x50, 0xa4, 0x11, 0xcf], [0x2f, 0x5e, 0xc8, 0x6a], [0x28, 0xd7, 0x07, 0x94]]
    tools.compare_2d(state, KAT3, 3)

    before4 = [[0xe0, 0xc8, 0xd9, 0x85], [0x92, 0x63, 0xb1, 0xb8], [0x7f, 0x63, 0x35, 0xbe], [0xe8, 0xc0, 0x50, 0x01]]
    state = s_box_sub(before4)
    KAT4 = [[0xe1, 0xe8, 0x35, 0x97], [0x4f, 0xfb, 0xc8, 0x6c], [0xd2, 0xfb, 0x96, 0xae], [0x9b, 0xba, 0x53, 0x7c]]
    tools.compare_2d(state, KAT4, 4)

    print(f'[END] Sub bytes Test')

def key_expansion(aes_key):
    w = [aes_key[0] << 24 | aes_key[1] << 16 | aes_key[2] << 8 | aes_key[3],
         aes_key[4] << 24 | aes_key[5] << 16 | aes_key[6] << 8 | aes_key[7],
         aes_key[8] << 24 | aes_key[9] << 16 | aes_key[10] << 8 | aes_key[11],
         aes_key[12] << 24 | aes_key[13] << 16 | aes_key[14] << 8 | aes_key[15]]
    temp = w[3]
    r_const_ptr = 0
    for x in range(4, 44, 1):

        if x % 4 == 0:
            temp = tools.rot_word_L(temp, 1)
            #print(f'[Debug] After RotWord(): 0x{temp:02x}')
            temp = sub_word(temp)
            #print(f'[Debug] After SubWord(): 0x{temp:02x}')
            #print(f'[Debug] Rcon: 0x{r_const[r_const_ptr]:02x}')
            temp ^= r_const[r_const_ptr]
            r_const_ptr += 1

            #print(f'[Debug] After XOR with Rcon: 0x{temp:02x}')

        temp ^= w[x - 4]
        #print(f'[Debug] After XOR with w[i-Nk]: 0x{temp:02x}')
        w.append(temp)

    key_out = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for i in range(len(key_out)):
        for j in range(len(key_out[0])):
            key_out[i][j] = w[i * len(key_out[0]) + j]

    return key_out

def key_expansion_test():
    print(f'[START] Key Expansion Test')
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    key = key_expansion(key)
    """
    KAT = [ 0x2b7e1516,0x28aed2a6,0xabf71588,0x09cf4f3c,
            0xa0fafe17,0x88542cb1,0x23a33939,0x2a6c7605,
            0xf2c295f2,0x7a96b943,0x5935807a,0x7359f67f,
            0x3d80477d,0x4716fe3e,0x1e237e44,0x6d7a883b,
            0xef44a541,0xa8525b7f,0xb671253b,0xdb0bad00,
            0xd4d1c6f8,0x7c839d87,0xcaf2b8bc,0x11f915bc,
            0x6d88a37a,0x110b3efd,0xdbf98641,0xca0093fd,
            0x4e54f70e,0x5f5fc9f3,0x84a64fb2,0x4ea6dc4f,
            0xead27321,0xb58dbad2,0x312bf560,0x7f8d292f,
            0xac7766f3,0x19fadc21,0x28d12941,0x575c006e,
            0xd014f9a8,0xc9ee2589,0xe13f0cc8,0xb6630ca6 ]
    tools.compare_word(key, KAT)

    tools.debug_print_arr_hex(key)
"""
    tools.debug_print_arr_2dhex(key)
    print(f'[END] Key Expansion Test')

def extract_key(key):

    byte_arr = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(4):
        converter = key[i].to_bytes(4, byteorder='big', signed=False)
        byte_arr[0][i] = int(converter[0])
        byte_arr[1][i] = int(converter[1])
        byte_arr[2][i] = int(converter[2])
        byte_arr[3][i] = int(converter[3])

    return byte_arr


def shift_rows(state):

    for i in range(1,4,1):
        word = tools.rot_word_L(state[i][0] << 24 | state[i][1] << 16 | state[i][2] << 8 | state[i][3], i)
        converter = word.to_bytes(4, byteorder='big', signed=False)
        state[i][0] = int(converter[0])
        state[i][1] = int(converter[1])
        state[i][2] = int(converter[2])
        state[i][3] = int(converter[3])

def shift_rows_inv(state):

    for i in range(1,4,1):
        word = tools.rot_word_R(state[i][0] << 24 | state[i][1] << 16 | state[i][2] << 8 | state[i][3], i)
        converter = word.to_bytes(4, byteorder='big', signed=False)
        state[i][0] = int(converter[0])
        state[i][1] = int(converter[1])
        state[i][2] = int(converter[2])
        state[i][3] = int(converter[3])

def test_enc():
    #key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    key = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f] #Test vector FIPS 197
    #state = [[0x32, 0x88, 0x31, 0xe0], [0x43, 0x5a, 0x31, 0x37], [0xf6, 0x30, 0x98, 0x07], [0xa8, 0x8d, 0xa2, 0x34]]
    state = [0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff] #Test vector FIPS197

    aes_keys = key_expansion(key)

    round_key = extract_key(aes_keys[0])
    state = tools.xor_2d(state, round_key)

    for curr_round in range(1, 11, 1):

        print(f'[Round {curr_round}]: Start of Round')
        tools.debug_print_arr_2dhex(state)
        print()

        print(f'[Round {curr_round}]: After SubBytes')
        s_box_sub(state)
        tools.debug_print_arr_2dhex(state)
        print()

        print(f'[Round {curr_round}]: After ShiftRows')
        shift_rows(state)
        tools.debug_print_arr_2dhex(state)
        print()

        if curr_round != 10:
            print(f'[Round {curr_round}]: After MixColumns')
            state = mix_cols(state)
            tools.debug_print_arr_2dhex(state)
            print()

        print(f'[Round {curr_round}]: Round key Value')
        round_key = extract_key(aes_keys[curr_round])
        state = tools.xor_2d(state, round_key)
        tools.debug_print_arr_2dhex(round_key)
        print()

    print(f'AES Complete')
    tools.debug_print_arr_2dhex(state)

def inv_shift_rows_test():
    KAT = [0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff]  # Test vector FIPS197
    state = [0x00, 0x44, 0x88, 0xcc], [0x11, 0x55, 0x99, 0xdd], [0x22, 0x66, 0xaa, 0xee], [0x33, 0x77, 0xbb, 0xff] #Test vector FIPS197


    print(f'[START] Inv Shift Rows Test')
    shift_rows(state)
    tools.debug_print_arr_2dhex(state)
    print()

    shift_rows_inv(state)
    tools.debug_print_arr_2dhex(state)

    tools.compare_2d(state, KAT, 0)
    print()


    print(f'[END] Inv Shift Rows Test')


if __name__ == '__main__':
    print("---- AES Encrypt Python Entry ----\r\n")

    #key_expansion_test()
    #mix_cols_test()
    #sub_bytes_test()

    #test_enc()
    #inv_mix_cols_test()
    inv_shift_rows_test()
























