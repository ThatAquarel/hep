import serial as ser
from scintillator_field.software.boundary_algorithm.detection import *



class DataReception:
    def __init__(self):
        serial = ser.Serial(port='COM3')

    def has_new_data(self):
        pass

    def get_data_from_arduino(self):
        pass

    def string_int32_to_scintillator_binary(self, string_int32):
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


        for pairx, pairy in zip(bits_x, bits_y):
            if (0, 0) in (pairx, pairy):
                raise ValueError("(0, 0) pair detected in scintillators")


        scintillators = [bits_x, bits_y]

        return scintillators
