import serial
import struct

import numpy as np

import os


class ArduinoData:
    def __new__(cls):
        # only a single instance is ever created
        # every future instance is actually first instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(ArduinoData, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.connected_to_arduino = False
    
    def connect_to_arduino(self):
        if os.name == "nt":
            dsrdtr = True
            port = "COM5"
        else:
            dsrdtr = False
            port = "/dev/ttyUSB0"

        self.arduino = serial.Serial(port=port, baudrate=115200, dsrdtr=dsrdtr)

        self.connected_to_arduino = True

    def arduino_has_data(self, mode):
        if mode=='debug':
            return True
        elif mode=='demo':
            return True
        elif mode=='data' and not self.connected_to_arduino:
            self.connect_to_arduino()
        #elif mode!='debug' and not self.connected_to_arduino:
        #    self.connect_to_arduino()
        return self.arduino.in_waiting >= 8
    
    def get_data_from_arduino(self):
        """
        Gather the data from Arduino
        """
        self.arduino.read_until(b"\x7E")
        value = self.arduino.read(4)
        if self.arduino.read(1) != b"\x7D":
            print("serial frame end error")

        (n,) = struct.unpack("<I", value)

        return [n]
    
    def format_print(self, value):
        lsb = value & 0xFFFFFF
        b1 = (lsb >> 16) & 0xFF
        b2 = (lsb >> 8) & 0xFF
        b3 = lsb & 0xFF

        print("receive trigger: SiPM status")
        print(f"    {b1:02x}          {b2:02x}          {b3:02x}")
        print(f"    {b1:08b}    {b2:08b}    {b3:08b}")
        print()