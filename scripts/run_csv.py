import csv
from email import message
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


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(("", 0))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.sendto(ZERO, (UDP_IP, UDP_PORT))
sleep(1)

# filename = "example.csv"
# filename = "data.csv"
filename = "data_1.csv"
with open(filename, "r") as f:
    # read csv and save to list
    reader = csv.reader(f)
    lines = list(reader)

lines = lines[1:]
lines = [[int(x) for x in line] for line in lines]
print(lines)

messages = [
    (
        create_message(
            line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]
        ),
        line[1] / 1000.0,
    )
    for line in lines
]
print(messages)

if False:
    for i in range(10):
        for message in messages:
            sock.sendto(message[0], (UDP_IP, UDP_PORT))
            sleep(message[1])
            # sleep(0.1)
else:
    for message in messages:
        sock.sendto(message[0], (UDP_IP, UDP_PORT))
        sleep(message[1])
        # sleep(0.1)
