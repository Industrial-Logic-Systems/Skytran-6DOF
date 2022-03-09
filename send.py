import socket
from time import sleep

UDP_IP = "<broadcast>"
UDP_PORT = 7408
MIN_SPEED = 0
MAX_SPEED = 100
MIN_VALUE = 0
MAX_VALUE = 200000


def scale(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    new_value = (((value - old_min) * new_range) / old_range) + new_min
    return int(new_value)


def bytes_from_int(i, scale_val=False):
    if scale_val:
        i = scale(i, MIN_SPEED, MAX_SPEED, MIN_VALUE, MAX_VALUE)
    i_bytes = bytearray(i.to_bytes(4, byteorder="big"))
    return i_bytes


def create_message(line, time, x, y, z, u, v, w):
    line = bytes_from_int(line)
    time = bytes_from_int(time)
    x = bytes_from_int(x, True)
    y = bytes_from_int(y, True)
    z = bytes_from_int(z, True)
    u = bytes_from_int(u, True)
    v = bytes_from_int(v, True)
    w = bytes_from_int(w, True)
    arr = [
        0x55,  # ConfirmCode
        0xAA,
        0x00,  # PassWord
        0x00,
        0x13,  # FunctionCode
        0x01,
        0x00,  # ObjectChannel
        0x01,
        0xFF,  # WhoAcceptCode
        0xFF,
        0xFF,  # WhoReplyCode
        0xFF,
        line[0],  # Line
        line[1],
        line[2],
        line[3],
        time[0],  # Time
        time[1],
        time[2],
        time[3],
        x[0],  # X
        x[1],
        x[2],
        x[3],
        y[0],  # Y
        y[1],
        y[2],
        y[3],
        z[0],  # Z
        z[1],
        z[2],
        z[3],
        u[0],  # U
        u[1],
        u[2],
        u[3],
        v[0],  # V
        v[1],
        v[2],
        v[3],
        w[0],  # W
        w[1],
        w[2],
        w[3],
        0x00,  # Base Dout
        0x00,
        0x00,  # DAC 1/2
        0x00,
        0x00,
        0x00,
    ]

    bytearr = bytearray(arr)

    return bytearr


RESET = bytearray(
    [
        0x55,
        0xAA,
        0x00,
        0x00,
        0x12,
        0x01,
        0x00,
        0x02,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0x00,
        0x00,
        0x00,
        0x01,
        0x00,
        0x00,
    ]
)
ZERO = create_message(1, 9, 0, 0, 0, 0, 0, 0)
# MESSAGE = create_message(1, 9, 100, 100, 100, 100, 100, 100)
MESSAGE = create_message(1, 9, 0, 100, 0, 100, 0, 100)
MESSAGE_3 = create_message(1, 9, 0, 100, 0, 100, 0, 100)
MESSAGE_4 = create_message(1, 9, 100, 0, 100, 0, 100, 0)
MESSAGE_1 = create_message(1, 9, 100, 100, 100, 0, 0, 0)
MESSAGE_2 = create_message(1, 9, 0, 0, 0, 100, 100, 100)
MESSAGE_5 = create_message(1, 9, 100000, 0, 0, 0, 0, 0)
MESSAGE_6 = create_message(1, 9, 101000, 0, 0, 0, 0, 0)

MESSAGE_7 = create_message(1, 9, 100, 100, 100, 100, 100, 100)
MESSAGE_8 = create_message(1, 9, 0, 0, 0, 0, 0, 00)

MESSAGE_9 = create_message(1, 9, 50, 50, 50, 50, 50, 50)
MESSAGE_10 = create_message(2, 9, 55, 55, 55, 55, 55, 55)

messages = [
    create_message(1, 9, 100, 100, 100, 100, 100, 100),
    create_message(2, 9, 50, 50, 50, 50, 50, 50),
    create_message(3, 9, 0, 100, 0, 100, 0, 100),
    create_message(4, 9, 50, 100, 50, 100, 50, 100),
    create_message(5, 9, 0, 0, 0, 0, 0, 0),
]

# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
# data = ":".join("{:02x}".format(x) for x in MESSAGE)
# print("message: %s" % data)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(("", 0))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.sendto(ZERO, (UDP_IP, UDP_PORT))
sleep(1)

if False:
    for message in messages:
        sock.sendto(message, (UDP_IP, UDP_PORT))
        sleep(0.1)
elif False:
    # sock.sendto(RESET, (UDP_IP, UDP_PORT))
    sock.sendto(MESSAGE_5, (UDP_IP, UDP_PORT))
    sleep(1)
    sock.sendto(MESSAGE_6, (UDP_IP, UDP_PORT))
    # sleep(5)
    # sock.sendto(ZERO, (UDP_IP, UDP_PORT))
else:
    for i in range(100):
        sock.sendto(MESSAGE_9, (UDP_IP, UDP_PORT))
        sleep(0.01)
        sock.sendto(MESSAGE_10, (UDP_IP, UDP_PORT))
        sleep(0.01)
