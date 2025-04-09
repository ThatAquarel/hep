import serial
import struct
import random   #for testing purposes

# windows
# ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, dsrdtr=True)

# mac/linux
ser = serial.Serial(port="/dev/cu.usbserial-14130", baudrate=115200)


def recv_packet(ser_handle):
    ser_handle.read_until(b"\x7E")
    value = ser_handle.read(4)

    if ser_handle.read(1) != b"\x7D":
        print("serial frame end error")

    (n,) = struct.unpack("<I", value)

    return n

def bit8(var):
    bit8 = 0
    for i in range(0, 8):

        new = (var >> 2 * i)&3

        if  new == 2:       #if it's 10

            bit8 += 2**i

        elif new != 1:

            return False
        
    return bit8

data = []
for i in range(12):
    packet = recv_packet(ser)
    x =  bit8(packet >> 16)
    y = bit8(packet & 65535)
    
    
    if not([x,y] in data):
        data.append([x,y])

data = []
for i in range(random.randint(5,10)):
    data.append([random.randint(0,255),random.randint(0,255)])


ser.close()
