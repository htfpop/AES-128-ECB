import tools

mix_col_matrix = [ [0x02, 0x03, 0x01, 0x01],
                   [0x01, 0x02, 0x03, 0x01],
                   [0x01, 0x01, 0x02, 0x03],
                   [0x03, 0x01, 0x01, 0x02] ]

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

def shift_rows(state):

    for i in range(1,4,1):
        word = tools.rot_word_L(state[i][0] << 24 | state[i][1] << 16 | state[i][2] << 8 | state[i][3], i)
        converter = word.to_bytes(4, byteorder='big', signed=False)
        state[i][0] = int(converter[0])
        state[i][1] = int(converter[1])
        state[i][2] = int(converter[2])
        state[i][3] = int(converter[3])



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

def extract_key(key):

    byte_arr = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(4):
        converter = key[i].to_bytes(4, byteorder='big', signed=False)
        byte_arr[0][i] = int(converter[0])
        byte_arr[1][i] = int(converter[1])
        byte_arr[2][i] = int(converter[2])
        byte_arr[3][i] = int(converter[3])

    return byte_arr

def populate_state(state, pt, curr_round):
    for col in range(len(state[0])):
        state[0][col] = pt[(col * 4) + (curr_round * 16)]
        state[1][col] = pt[(col * 4 + 1) + (curr_round * 16)]
        state[2][col] = pt[(col * 4 + 2) + (curr_round * 16)]
        state[3][col] = pt[(col * 4 + 3) + (curr_round * 16)]

def aes_encrypt(pt,key):
    ciphertext = 0x00
    key_schedule = key_expansion(key)
    num_blocks = int(len(pt) / 16)
    curr_round = 0

    for i in range(num_blocks):
        state = [[0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00]]
        populate_state(state, pt, curr_round)

        round_key = extract_key(key_schedule[0])
        state = tools.xor_2d(state, round_key)
        for aes_round in range(1, 11, 1):
            print(f'[ENCRYPT]: round{aes_round}: Start of Round')
            tools.debug_print_arr_2dhex_1line(state)
            print()

            print(f'[ENCRYPT]: round{aes_round}: After SubBytes')
            s_box_sub(state)
            tools.debug_print_arr_2dhex_1line(state)
            print()

            print(f'[ENCRYPT]: round{aes_round}: After ShiftRows')
            shift_rows(state)
            tools.debug_print_arr_2dhex_1line(state)
            print()

            if aes_round != 10:
                print(f'[ENCRYPT]: round{aes_round}: After MixColumns')
                state = mix_cols(state)
                tools.debug_print_arr_2dhex_1line(state)
                print()

            print(f'[ENCRYPT]: round{aes_round}: Round key Value')
            round_key = extract_key(key_schedule[aes_round])
            state = tools.xor_2d(state, round_key)
            tools.debug_print_arr_2dhex_1line(round_key)
            print()

        print(f'AES Encrypt Complete')
        tools.debug_print_arr_2dhex(state)

        curr_round += 1


    return ciphertext
def aes_main(pt, key):
    testpt = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff]
    testkey = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]

    test1 = bytearray(testpt)
    test2 = bytearray(testkey)

    #ciphertext = aes_encrypt(pt,key)
    ciphertext = aes_encrypt(test1, test2)

    #todo call aes decrypt
























