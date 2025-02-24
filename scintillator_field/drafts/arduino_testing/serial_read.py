import serial
import struct


class commands:
    NUL = 0x00

    SYN = 0xAB
    ACK = 0x4B
    NAK = 0x5A
    ERR = 0x3C

    DATA = 0x01
    # HOME_CARRIAGE = 0x02
    # HOME_SERVO = 0x03
    # MOVE_CARRIAGE = 0x04
    # MOVE_SERVO = 0x05


class packet_t:
    cmd = 0
    buffer = 0

    def __init__(self, buffer=b"", cmd=commands.NUL):
        self.buffer = buffer
        self.cmd = cmd


def send_packet(ser_handle, packet: packet_t):
    packet_bytes = struct.pack(
        f"<xBBB{len(packet.buffer)}sBx",
        0x7E,  # U8 start of packet flag
        packet.cmd & 0xFF,  # U8 command
        len(packet.buffer) & 0xFF,  # U8 length of payload
        packet.buffer,  # U8 payload[len]
        0x7D,  # U8 end of packet flag
    )

    print(packet_bytes)
    ser_handle.write(packet_bytes)


def recv_packet(ser_handle):
    ser_handle.read_until(b"\x7E")

    command, length = struct.unpack("<cB", ser_handle.read(2))
    payload = b""
    if length:
        payload = struct.unpack(f"<{length}s", ser_handle.read(length))

    if ser_handle.read(1) != b"\x7D":
        print("serial frame end error")

    return packet_t(payload, ord(command))


ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, dsrdtr=True)


send_packet(ser, packet_t(cmd=commands.RESET))
print(recv_packet(ser).cmd)

# send_packet(ser, packet_t(cmd=commands.HOME_CARRIAGE))
# print(recv_packet(ser).cmd)

# send_packet(ser, packet_t(cmd=commands.HOME_SERVO))
# print(recv_packet(ser).cmd)

# send_packet(
#     ser,
#     packet_t(
#         buffer=struct.pack(
#             "<9B",
#             *[
#                 0,
#             ]
#             * 9,
#         ),
#         cmd=commands.MOVE_SERVO,
#     ),
# )
# print(recv_packet(ser).cmd)

ser.close()