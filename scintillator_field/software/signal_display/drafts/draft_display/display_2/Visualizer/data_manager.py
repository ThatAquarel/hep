# from scintillator_field.software.boundary_algorithm.detection import *
#import scintillator_field.software.boundary_algorithm.detection as d
from detection import *
import serial
import struct
import os

from datetime import datetime


import numpy as np
class test:
    def __init__(self):
        dsrdtr = False
        port = "/dev/ttyUSB0"

        if os.name == "nt":
            dsrdtr = True
            port = "COM5"

        self.arduino = serial.Serial(port=port, baudrate=115200, dsrdtr=dsrdtr)



        self.detection_algorithm = Detection()
        self.data = []
        self.reset()

        #self.testing()  #For real data, remove this line
        


    def has_data(self):
        """
        Check if the Arduino has data
        """
        return self.arduino.in_waiting >= 8
    
    def get_data_from_arduino(self):
        """
        Gather the data from Arduino
        """
        self.arduino.read_until(b"\x7E")
        value = self.arduino.read(4)
        if self.arduino.read(1) != b"\x7D":
            print("serial frame end error")

        remaining = self.arduino.in_waiting
        self.arduino.read(remaining)

        (n,) = struct.unpack("<I", value)

        return n

    def reset(self):
        """
        Reset Aljoscha's code, since we use different values
        """

        # Global variables
        self.detection_algorithm.level_count = 1
        self.detection_algorithm.n = 2*60 * 0.1 # Sideview length of scintillator in unit x


        # These values are used for x perspective
        self.detection_algorithm.upper_side_views = [(0, self.detection_algorithm.n)] # (start, end) coordinates for each level 
        self.detection_algorithm.lower_side_views = [(0, self.detection_algorithm.n)]

        self.detection_algorithm.plate_thickness = 10 * 0.1# In unit x
        self.detection_algorithm.intra_level_gap = 2 * 0.1#Actual physical gap between each level, in unit x
        self.detection_algorithm.inter_level_gap = self.detection_algorithm.plate_thickness + self.detection_algorithm.intra_level_gap # Adjusted inter level gap for computation 

        self.detection_algorithm.half_gap_size =  162/2 * 0.1# In unit x
        self.detection_algorithm.top_half_gap = self.detection_algorithm.half_gap_size + self.detection_algorithm.plate_thickness + self.detection_algorithm.intra_level_gap
        self.detection_algorithm.bottom_half_gap = self.detection_algorithm.half_gap_size
        self.detection_algorithm.gap_line = 0
        self.detection_algorithm.highest_point = self.detection_algorithm.half_gap_size + 5*self.detection_algorithm.intra_level_gap + 6*self.detection_algorithm.plate_thickness # Values custom set to this detector
        self.detection_algorithm.lowest_point = -self.detection_algorithm.highest_point

    def update_data(self,raw_data):
        """
        transform data ready to be interpreted by the visualizer, then update self.data
        """
        
        #bit24 = raw_data & 0xffffff     #turn from 32bit to 24 bit
        

        #cooked_data = self.interpret_raw_data(bit24) 

        f_sc_idx = [
        [(21,20),(16,17),(13,12),(8,9),(0,1),(5,4),],
        [(22,23),(18,19),(15,14),(11,10),(2,3),(6,7),],
        ]

        k = np.array([(raw_data & (2**i)) >> i for i in range(24)])[f_sc_idx]

        cooked_data = [[(int(k[0]), int(k[1])) for k in k[0]], [(int(k[0]), int(k[1])) for k in k[1]]]

        algorithmized = self.detection_algorithm.scintillators_to_bounds(cooked_data)

        if not algorithmized:
            return

        self.reset()

        time = datetime.now()

        new_hull_bounds = self.transform_coordinates(algorithmized[0])
        new_fan_out_lines = self.transform_coordinates_fanned(algorithmized[1])

        bit24 = raw_data & 0xffffff
        
        point = [new_hull_bounds, new_fan_out_lines, cooked_data, bit24, time]

        self.data.append(point)





    def interpret_raw_data(self,bin):
        """
        change the format to be inputted into Aljoscha's code
        """

        x = bin & 3355443   #& operator on 0b001100110011001100110011
        y = bin & 13421772  #& operator on 0b110011001100110011001100

        bit = 12
        list_x = []
        list_y = []
        for i in range(0, bit, 2):
            last_two_x = (x >> (i * 2))
            list_x.append(((last_two_x & 2) >> 1, last_two_x & 1))

            last_two_x = (y >> (i * 2 + 2))
            list_y.append(((last_two_x & 2) >> 1, last_two_x & 1))

        return [list_x,list_y]
    
        #transforming coordinates
    def transform_coordinates(self,data):
        """
        transform into my coordinate system
        """
        translate_x = -self.detection_algorithm.n / 2
        translate_y = -self.detection_algorithm.n/2
        z_scale = 1

        list = []
        for coordinates in data:
            x = (coordinates[0] + translate_x) * -1
            y = (coordinates[1] + translate_y) * 1
            z = (coordinates[2] + self.detection_algorithm.half_gap_size - self.detection_algorithm.inter_level_gap + self.detection_algorithm.plate_thickness) / z_scale
            list.append((x,y,z))

        return list

    def transform_coordinates_fanned(self,data):
        """
        Transform the fanning part into my coordinate system
        """
        list = []
        for pair in data:
            list.append(self.transform_coordinates(pair))

        return list
    

    def testing(self):
        scintillator_1= [[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)],[(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)]]
        scintillator_2 = [[(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)], [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]]
        
        # self.update_data(0b101101010101101011010110)     
        # self.update_data(0b111101100101111101101111)
        # self.update_data(0b101111011110111001011101)
        # self.update_data(0b010101010101010101010101)
        # self.update_data(0b010111011110100110011101)

        self.update_data(0b011011010110101011010110)
        self.update_data(0b100110101101010101101001)
        self.update_data(0b100101101010011101011001)
        
        # self.update_data(0b101010101010101010101010)
        # self.update_data(0b010101010101010101010101)


