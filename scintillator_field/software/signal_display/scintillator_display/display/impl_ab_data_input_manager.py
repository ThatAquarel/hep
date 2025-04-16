import os
import struct

from datetime import datetime

import serial
import numpy as np

from scintillator_display.math.convex_hull import ConvexHullDetection as Detection


class Data:
    def __init__(self, impl_constant, impl, debug=True):
        self.debug = debug
        self.impl = impl # "a" or "b"
        self.data = []
        self.detection_algorithm = Detection(impl_constant=impl_constant)



        if self.debug:
            self.testing()
            pass
        else:
            if os.name == "nt":
                dsrdtr = True
                port = "COM5"
            else:
                dsrdtr = False
                port = "/dev/ttyUSB0"

            self.arduino = serial.Serial(port=port, baudrate=115200, dsrdtr=dsrdtr)


    def arduino_has_data(self):
        if self.debug:
            if self.impl == "b":
                return self.impl_b_testing
            elif self.impl == "a":
                return False
        return self.arduino.in_waiting >= 8
    
    def get_data_from_arduino(self):
        if self.debug:
            self.impl_b_testing = False
            return 1431655765
        """
        Gather the data from Arduino
        """
        self.arduino.read_until(b"\x7E")
        value = self.arduino.read(4)
        if self.arduino.read(1) != b"\x7D":
            print("serial frame end error")

        (n,) = struct.unpack("<I", value)

        return n
    
    def cook_data_into_scintillators(self, raw_data):
        """
        transform data ready to be interpreted by the display, then update self.data
        """
        
        f_sc_idx = [
        [(21,20),(16,17),(13,12),(8,9),(0,1),(5,4),],
        [(22,23),(18,19),(15,14),(11,10),(2,3),(6,7),],
        ]

        k = np.array([(raw_data & (2**i)) >> i for i in range(24)])[f_sc_idx]

        cooked_data = [[(int(k[0]), int(k[1])) for k in k[0]], [(int(k[0]), int(k[1])) for k in k[1]]]

        return cooked_data
    
    
    def format_print(self, value):
        lsb = value & 0xFFFFFF
        b1 = (lsb >> 16) & 0xFF
        b2 = (lsb >> 8) & 0xFF
        b3 = lsb & 0xFF

        print("receive trigger: SiPM status")
        print(f"    {b1:02x}          {b2:02x}          {b3:02x}")
        print(f"    {b1:08b}    {b2:08b}    {b3:08b}")
        print()
    
    def impl_a_transform_data(self, raw_data):

        cooked_data = self.cook_data_into_scintillators(raw_data)
        self.cooked_data = cooked_data
        
        algorithmized = self.detection_algorithm.scintillators_to_bounds(cooked_data)

        if self.impl == "b":
            if algorithmized == None:
                return False
            return True
        
        if not algorithmized:
            return
        
        if algorithmized == None:
            return

        self.detection_algorithm.reset_to_initial_values()

        time = datetime.now()

        new_hull_bounds = self.transform_coordinates_impl_a(algorithmized[0])
        new_fan_out_lines = self.transform_coordinates_fanned_impl_a(algorithmized[1])

        bit24 = raw_data & 0xffffff
        
        point = [new_hull_bounds, new_fan_out_lines, cooked_data, bit24, time]

        self.data.append(point)


    def transform_coordinates_impl_a(self,data):
        """
        transform into my coordinate system
        """
        translate_x = -self.detection_algorithm.n / 2
        translate_y = -self.detection_algorithm.n/2
        z_scale = 1

        lst = []
        for i, coordinates in enumerate(data):
            x = (coordinates[0] + translate_x) * -1
            y = (coordinates[1] + translate_y) * 1
            z = (coordinates[2] + self.detection_algorithm.half_gap_size - self.detection_algorithm.inter_level_gap + self.detection_algorithm.plate_thickness) / z_scale
            lst.append((x,y,z))

        return lst

    def transform_coordinates_fanned_impl_a(self,data):
        """
        Transform the fanning part into my coordinate system
        """
        lst = []
        for i, pair in enumerate(data):
            lst.append(self.transform_coordinates_impl_a(pair))

        return lst
    
    def testing(self):
        if self.impl == "b":
            self.impl_b_testing = True
        elif self.impl == "a":
            self.impl_a_transform_data(0b011011010110101011010110)
            self.impl_a_transform_data(0b100110101101010101101001)
            self.impl_a_transform_data(0b100101101010011101011001)
