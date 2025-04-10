import serial
import struct


# windows
# ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, dsrdtr=True)

# mac/linux
ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)


def recv_packet(ser_handle):
    ser_handle.read_until(b"\x7E")
    value = ser_handle.read(4)

    if ser_handle.read(1) != b"\x7D":
        print("serial frame end error")

    (n,) = struct.unpack("<I", value)

    return n

for _ in range(1024):
    print(recv_packet(ser))

ser.close()

