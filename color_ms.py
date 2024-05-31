# Based on code from https://realpython.com/python-sockets/
# Written By: Ito Christine

import socket

COLORS = {
    "Brown": "#8B6C5C",
    "Blue": "#375362",
    "Pink": "#EBB8DD"
}


def display_colors():
    """returns a list of color options"""
    list = "`".join(COLORS.keys())
    return list


def save_color(color_pref):
    """returns python code to change background color in tkinter GUI"""
    color_file = open("color.txt", "w")
    color_file.write(color_pref)


def get_color():
    """saves user's preferred color for the background from save_color"""
    with open("color.txt", "r", encoding='utf-8') as f:
        data = f.read()
    return data    


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 6255  # Port to listen on (non-privileged ports are > 1023)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                if data == 'display':
                    colors = display_colors()
                    conn.sendall(colors.encode())

                if data == 'Brown':
                    save_color(COLORS[data])
                    success = "1"
                    conn.sendall(success.encode())

                if data == 'Blue':
                    save_color(COLORS[data])
                    success = "1"
                    conn.sendall(success.encode())

                if data == 'Pink':
                    save_color(COLORS[data])
                    success = "1"
                    conn.sendall(success.encode())

                if data == 'getcolor':
                    color_selected = get_color()
                    conn.sendall(color_selected.encode())