import socket

UDP_PORT = 7408

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
sock.bind(("", UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print("addr: ", addr)
    # print("message:", data)
    # data = str(data)
    # data = data.replace("\\x", " ")
    # data = data.replace("b'U", "")
    # data = data.replace("'", "")
    # data = ":".join(hex(x)[2:] for x in data)
    data = ":".join(f"{x:02x}" for x in data)
    print("string:", data)
