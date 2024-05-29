# Based off of: https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python
import socket
SERVER_IP = "127.0.0.1"
PORT = 8300
# Port to listen on (non-privileged ports are > 1023)


def get_info():
    return "Welcome to the Foodie App!\n\n" \
                "Selecting add/edit/delete on the Home Page will allow you to make changes to the Pantry and/or Recipe Book.\n" \
                "Selecting Pantry will allow you to view and add/edit/delete ingredients only.\n" \
                "Selecting Recipe Book will allow you to view and add/edit/delete recipes only.\n" \
                "Selecting Welcome Page will reopen this text box.\n" \
                "Selecting Home on any page will bring you back to the Home Page.\n\n" \
                "FAQ:\n" \
                "Can I recover a deleted item?\n" \
                "No, all deletions are permanent.\n\n" \
                "How do I add a new ingredient?\n" \
                "To add a new ingredient, please select Pantry -> Add. " \
                "Alternatively, you may select Add -> Ingredient on the Homepage.\n"


def get_skip():
    with open('skip.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def edit_skip(val):
    with open('skip.txt', 'w', encoding='utf-8') as f:
        f.write(val)
    return "1"


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, PORT))
    server.listen(0)
    print(f"Listening on {SERVER_IP}:{PORT}")
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")

            if request.lower() == "exit":
                client_socket.send("closed".encode("utf-8"))
                break

            if not request:
                break

            print(f"Received: {request}")
            request = request.split("`")

            if request[0] == "read":
                response = get_info().encode("utf-8")
            elif request[0] == "getskip":
                response = get_skip().encode("utf-8")
            elif request[0] == "editskip":
                response = edit_skip(request[1]).encode("utf-8")
            else:
                response = "invalid input".encode("utf-8")
            client_socket.send(response)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection to client closed")
        server.close()


while True:
    run_server()