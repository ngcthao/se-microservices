# Based off of: https://www.datacamp.com/tutorial/a-complete-guide-to-socket-programming-in-python
import json
import os
from json import JSONDecodeError
import pandas as pd
import socket
SERVER_IP = "127.0.0.1"
PORT = 8400
# Port to listen on (non-privileged ports are > 1023)


class Ingredient:
    def __init__(self, args):
        self.name = args[0].title()
        self.count = args[1]
        self.units = args[2].lower()


class Pantry:
    def __init__(self):
        self.file = 'ingredients.json'

    def new_ingredient(self, args):
        item = Ingredient(args)
        ingredient = {
            item.name: {
                "quantity": item.count,
                "unit of measurement": item.units
                        }
        }

        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(ingredient, f, indent=4)
            else:
                data.update(ingredient)
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, sort_keys=True)
        else:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(ingredient, f, indent=4)

        return "1"

    def read_ingredients(self):
        output = ""
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                pass
            else:
                data = json.dumps(data)
                data = json.loads(data)
                output = pd.DataFrame(data).transpose().to_string()
            finally:
                return output

    def edit_ingredient(self, args):
        if args[0] == "":
            return "0"
        self.delete_ingredient(args[0])
        self.new_ingredient(args[1:])
        return "1"

    def delete_ingredient(self, arg):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                pass
            else:
                data = pd.DataFrame(data).transpose()
                data = data.drop(index=arg.title())
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(data.transpose().to_dict(), f, indent=4, sort_keys=True)
            finally:
                return "1"

    def dropdown_display(self):
        output = ""
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                pass
            else:
                data = json.dumps(data)
                data = json.loads(data)
                output = "`".join(data.keys())
            finally:
                return output


def run_server():
    pantry = Pantry()
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

            if request[0] == "new":
                response = pantry.new_ingredient(request[1:])
            elif request[0] == "read":
                response = pantry.read_ingredients()
            elif request[0] == "edit":
                response = pantry.edit_ingredient(request[1:])
            elif request[0] == "delete":
                response = pantry.delete_ingredient(request[1])
            elif request[0] == "dropdown":
                response = pantry.dropdown_display()
            else:
                response = "invalid input"

            print(f"Sending: {response}\n\n")
            client_socket.send(response.encode("utf-8"))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection to client closed")
        server.close()


while True:
    run_server()
