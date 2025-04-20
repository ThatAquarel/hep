import struct

import serial


ser = serial.Serial(port="COM5", baudrate=115200, dsrdtr=True)

ser.read_until(b"\x7E")
(n,) = struct.unpack(f"<I", ser.read(4))
if ser.read(1) != b"\x7D":
    print("serial frame end error")

print(n)