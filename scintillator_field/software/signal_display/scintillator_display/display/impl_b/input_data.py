import serial
# from scintillator_field.software.boundary_algorithm.detection import *
from scintillator_display.math.convex_hull import ConvexHullDetection as Detection

import struct

import os
import numpy as np

class DataReception:
    def __init__(self, debug=True):
        self.debug = debug

        if debug:
            self.testing()
        else:
            dsrdtr = False
            port = "/dev/ttyUSB0"

            if os.name == "nt":
                dsrdtr = True
                port = "COM4"

            self.arduino = serial.Serial(port=port, baudrate=115200, dsrdtr=dsrdtr)

        self.detection_algorithm = Detection()

    def testing(self):
        self.to_create_testing = True

    def has_new_data(self):
        if self.debug:
            return self.to_create_testing

        return self.arduino.in_waiting >= 8
        

    def format_print(self, value):
        lsb = value & 0xFFFFFF
        b1 = (lsb >> 16) & 0xFF
        b2 = (lsb >> 8) & 0xFF
        b3 = lsb & 0xFF

        print("receive trigger: SiPM status")
        print(f"    {b1:02x}          {b2:02x}          {b3:02x}")
        print(f"    {b1:08b}    {b2:08b}    {b3:08b}")
        print()

    def get_data_from_arduino(self):
        if self.debug:
            self.to_create_testing = False
            return 1431655765

        self.arduino.read_until(b"\x7E")
        value = self.arduino.read(4)
        if self.arduino.read(1) != b"\x7D":
            print("serial frame end error")

        #remaining = self.arduino.in_waiting
        #self.arduino.read(remaining)

        (n,) = struct.unpack("<I", value)

        #self.format_print(n)
        return n

        # string_int = self.arduino.readline()
        # print(string_int, "a")
        # return string_int

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

        scintillators = [bits_x, bits_y]

        return scintillators

    def is_valid_data(self, data):

        #print(data)

        self.scintillators = self.string_int32_to_scintillator_binary(data)


        f_sc_idx = [
        [(21,20),(16,17),(13,12),(8,9),(0,1),(5,4),],
        [(22,23),(18,19),(15,14),(11,10),(2,3),(6,7),],
        ]

        k = np.array([(data & (2**i)) >> i for i in range(24)])[f_sc_idx]

        k = [[(int(k[0]), int(k[1])) for k in k[0]], [(int(k[0]), int(k[1])) for k in k[1]]]

        bl4 = k

        #print(self.scintillators)
        #print(bl4)
        #print()

        self.scintillators = bl4


        #for pairx, pairy in zip(self.scintillators[0], self.scintillators[1]):
        #    if (0, 0) in (pairx, pairy):
        #        return False

        if self.detection_algorithm.scintillators_to_bounds(self.scintillators) == None:
            return False
        
        return True