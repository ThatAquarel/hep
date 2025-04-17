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
    
    
    def format_print(self, value):
        lsb = value & 0xFFFFFF
        b1 = (lsb >> 16) & 0xFF
        b2 = (lsb >> 8) & 0xFF
        b3 = lsb & 0xFF

        print("receive trigger: SiPM status")
        print(f"    {b1:02x}          {b2:02x}          {b3:02x}")
        print(f"    {b1:08b}    {b2:08b}    {b3:08b}")
        print()
    
    
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
    
    def is_valid_data(self, data=None):
        self.raw_data = self.get_data_from_arduino() if data==None else data
        self.cooked_data = self.cook_data_into_scintillators(self.raw_data)
        self.scintillator_bounds = self.detection_algorithm.scintillators_to_bounds(self.cooked_data)

        if self.impl == "a":
            if not self.scintillator_bounds:
                return
            elif self.scintillator_bounds == None:
                return
        elif self.impl == "b":
            if self.scintillator_bounds == None:
                return False
            return True


    def scale_hull_bounds(self, hull_bounds):
        '''
        hull_bounds = [1, 2, 3, 4, 5, 6, 7, 8]
        '''

        idx = [[0, 7],[1, 6],[2, 5],[3, 4],]
        fan = np.array(hull_bounds)[idx]
        scale_factor = 75 if self.impl == "a" else 700
        fan_vec = np.array([scale_factor*(p[0]-p[1])/np.linalg.norm(p[0]-p[1]) for p in fan])
        
        scaled_p0 =  fan_vec[0]+hull_bounds[0]
        scaled_p1 =  fan_vec[1]+hull_bounds[1]
        scaled_p2 =  fan_vec[2]+hull_bounds[2]
        scaled_p3 =  fan_vec[3]+hull_bounds[3]
        scaled_p4 = -fan_vec[3]+hull_bounds[4]
        scaled_p5 = -fan_vec[2]+hull_bounds[5]
        scaled_p6 = -fan_vec[1]+hull_bounds[6]
        scaled_p7 = -fan_vec[0]+hull_bounds[7]


        scaled_hull_bounds = [scaled_p0, scaled_p1,
                              scaled_p2, scaled_p3,
                              scaled_p4, scaled_p5,
                              scaled_p6, scaled_p7]

        return scaled_hull_bounds
        
    
    def transform_data_per_impl(self):
        hull_bounds = self.scintillator_bounds

        if self.impl == "a":
            time = datetime.now()

            new_hull_bounds = self.transform_coordinates_impl_a(hull_bounds)
            #new_fan_out_lines = self.transform_coordinates_fanned_impl_a(fan_out)

            bit24 = self.raw_data & 0xffffff
            
            #point = [new_hull_bounds, new_fan_out_lines, self.cooked_data, bit24, time]
            point = [new_hull_bounds, self.cooked_data, bit24, time]

            self.data.append(point)
            
        elif self.impl == "b":
            hull_bounds = np.array(hull_bounds) - np.array([0, 0, 162/2])
            return np.array(hull_bounds).astype(np.float32)#, np.array(fan_out).astype(np.float32)


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

    
    def testing(self):
        if self.impl == "b":
            self.impl_b_testing = True
        elif self.impl == "a":
            test_data = [0b011011010110101011010110,
                    0b100110101101010101101001,
                    0b100101101010011101011001,
                    1431655765]
            for data in test_data:
                self.is_valid_data(data)
                self.transform_data_per_impl()
