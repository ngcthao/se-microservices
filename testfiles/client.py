# Hw 4 - Ngoc-Thao Ly
# Client

import socket

HOST = "127.0.0.1"
PORT = 10485

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"A message from CS361")
    data = s.recv(1024)

print(f"Received from server: {data!r}")