def interpret_raw_data(bin):
    x = bin & 3355443   #& operator on 0b001100110011001100110011
    y = bin & 13421772  #& operator on 0b110011001100110011001100

    bit = 12
    bitminus2 = bit - 2
    list_x = []
    list_y = []
    for i in range(0, bit, 2):
        last_two_x = (x >> (i * 2))
        list_x.append(((last_two_x & 2) >> 1, last_two_x & 1))

        last_two_x = (y >> (i * 2 + 2))
        list_y.append(((last_two_x & 2) >> 1, last_two_x & 1))

    return [list_x,list_y]


def interpet(num_int):
    binary_list = []
    for i in range(32):
        '''
        (num_int & (2**i))   bitwise and on num_int for each bit position within the binary
            separates a number into binary, num if 1, 0 if 0 at a given spot
        >> i   right shift binary by position in binary
            turns each non-zero binary number into 1
        '''
        binary_list.append((num_int & (2**i)) >> i)


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


    # for pairx, pairy in zip(bits_x, bits_y):
    #     if (0, 0) in (pairx, pairy):
    #         raise ValueError("(0, 0) pair detected in scintillators")

    return [bits_x, bits_y]





...