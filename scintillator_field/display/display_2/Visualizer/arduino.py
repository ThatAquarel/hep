import serial
import struct


# windows
# ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, dsrdtr=True)

# mac/linux
ser = serial.Serial(port="/dev/cu.usbserial-14330", baudrate=115200)


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

        if  new == 2:

            bit8 += 2**i

        elif new != 1:

            return False
        
    return bit8

def bin_to_list(bin):
    bit = len(bin)      #12
    list = []
    for i in range(bit//2):

        first_two  = (bin >> ((bit-2) - 2 * i)) & 3

        if first_two == 2:

            list.append((1,0))

        elif first_two == 1:

            list.append((0,1))
        
        else:
            return False    #error
    
    return list

def interpret_raw_data(bin):
    x = bin >> 12   #first 12 nums
    y = bin & 4095

    return [bin_to_list(x),bin_to_list(y)]

for _ in range(12):
    packet = recv_packet(ser)
    
    print(interpret_raw_data(packet))




ser.close()