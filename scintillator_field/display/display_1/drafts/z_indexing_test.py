import numpy as np

def string_int32_to_scintillator_binary(string_int32):
    num_int = int(string_int32)

    binary_list = []
    for i in range(32):
        '''
        (num_int & (2**i))   bitwise and on num_int for each bit position within the binary
            separates a number into binary, num if 1, 0 if 0 at a given spot
        >> i   right shift binary by position in binary
            turns each non-zero binary number into 1
        '''
        binary_list.append((num_int & (2**i)) >> i)
    
    bl2 = []
    for i in range(24): # only first 24 bits are relevant
        '''
        (num_int & (2**i))   bitwise and on num_int for each bit position within the binary
            separates a number into binary, num if 1, 0 if 0 at a given spot
        >> i   right shift binary by position in binary
            turns each non-zero binary number into 1
        '''
        bl2.append((num_int & (2**i)) >> i)

    bl3 = np.array([(num_int & (2**i)) >> i for i in range(24)])

    
    print(format(string_int32, '032b'))
    print(".", binary_list)

    b2 = np.array(binary_list[::-1])

    print(".", b2)

    b3 = b2[8:]
    print(".", b3, len(b3))

    print("a", binary_list[24::-1])

    b4 = b3[::-1]
    print(".", b4)
    print("b", binary_list[24::-1][::-1])

    idx = [5,4,7,6,0,1,2,3,8,9,10,11,13,12,15,14,16,17,18,19,21,20,23,22]
    b5 = b4[idx]
    print(".", b5)
    print("c", np.array(binary_list[24::-1][::-1])[idx])

    b6 = b5[::-1]
    print(".", b6)
    print("d", np.array(binary_list[24::-1][::-1])[idx][::-1])

    print("e", np.array(binary_list)[24::-1][::-1][idx][::-1])
    print("f", np.array(binary_list)[:-8][idx][::-1])
    k_idx = idx[::-1]
    print("g", np.array(binary_list)[:-8][k_idx])

    f_idx = [22,23,20,21,19,18,17,16,14,15,12,13,11,10,9,8,3,2,1,0,6,7,4,5]
    print("h", np.array(binary_list)[:-8][f_idx])

    print("i", np.array(bl2)[f_idx])
    print("j", bl3[f_idx])

    sc_idx = [
                [(3,2),(7,6),(11,10),(15,14),(19,18),(23,22),],
                [(0,1),(4,5),(8,9),(12,13),(16,17),(20,21),]
             ]
    
    print("k", bl3[f_idx][sc_idx])

    f_sc_idx = [
        [(21,20),(16,17),(13,12),(8,9),(0,1),(5,4),],
        [(22,23),(18,19),(15,14),(11,10),(2,3),(6,7),],
    ]

    print("l", bl3[f_sc_idx])

    bl4 = np.array([(num_int & (2**i)) >> i for i in range(24)])[f_sc_idx]
    print("m", bl4)

    sc = [
        [
            (b6[3],b6[2]),
            (b6[7],b6[6]),
            (b6[11],b6[10]),
            (b6[15],b6[14]),
            (b6[19],b6[18]),
            (b6[23],b6[22]),
        ],
        [
            (b6[0],b6[1]),
            (b6[4],b6[5]),
            (b6[8],b6[9]),
            (b6[12],b6[13]),
            (b6[16],b6[17]),
            (b6[20],b6[21]),
        ],
    ]
    print(np.array(sc))



    binary_list = binary_list[:24] # removes unnecessary bits from binary list


    bits_x = []
    bits_y = []

    for i in range((len(binary_list)//2)):
        '''
        for every first two members of binary_list, those are x_views
        for every second two members of binary_list, those are y_views

        puts these into tuples of two due to options from ([a, not b], [not a, b], [a, b], [not a, not b])
        '''
        if i%2==0:
            bits_x.append((binary_list[2*i], binary_list[2*i+1]))
        elif i%2==1:
            bits_y.append((binary_list[2*i], binary_list[2*i+1]))

    scintillators = [bits_x, bits_y]

    return scintillators

string_int32_to_scintillator_binary(1431655765)