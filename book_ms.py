import json
import os
from json import JSONDecodeError
import pandas as pd
import socket
SERVER_IP = "127.0.0.1"
PORT = 8100
# Port to listen on (non-privileged ports are > 1023)


class Recipe:
    def __init__(self, args):
        self.name = args[0].title()
        self.description = args[1]


class RecipeBook:
    def __init__(self):
        self.file = 'recipes.json'

    def new_recipe(self, args):
        item = Recipe(args)
        recipe = {
            item.name: {
                "description": item.description
            }
        }
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(recipe, f, indent=4)
            else:
                data.update(recipe)
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, sort_keys=True)
        else:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(recipe, f, indent=4)
        return "1"

    def read_recipes(self):
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
                dframe = pd.DataFrame(data)
                output = []
                for col in dframe.columns:
                    output.append(col)
            finally:
                return "`".join(output)

    def search_recipes(self, name):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = json.dumps(data)
            data = json.loads(data)
            output = [name, data[name]["description"]]
            return "`".join(output)


def run_server():
    recipe = RecipeBook()
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
                response = recipe.new_recipe(request[1:]).encode("utf-8")
            elif request[0] == "read":
                response = recipe.read_recipes().encode("utf-8")
            elif request[0] == "search":
                response = recipe.search_recipes(request[1]).encode("utf-8")
            elif request[0] == "edit":
                pass
            elif request[0] == "delete":
                pass
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