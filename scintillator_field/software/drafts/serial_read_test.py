import struct
import serial


ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)

ser.read_until(b"\x7E")

(n,) = struct.unpack("<I", ser.read(4))
if ser.read(1) != b"\x7D":
    raise BufferError("End flag error")

print(n)

def format_print(value):
    lsb = value & 0xFFFFFF
    b1 = (lsb >> 16) & 0xFF
    b2 = (lsb >> 8) & 0xFF
    b3 = lsb & 0xFF
    print(f"    {b1:02x}          {b2:02x}          {b3:02x}")
    print(f"    {b1:08b}    {b2:08b}    {b3:08b}")

format_print(n)
