import threading
import json


class ConnSocket(threading.Thread):
    def __init__(self, client_conn, addr, server):
        super().__init__()
        self.client_conn = client_conn
        self.addr = addr
        self.server = server

    def run(self):
        while True:
            data = self.client_conn.recv(1024).decode()

            if data:
                data = json.loads(data)
                command_id = int(data["command_id"])

                if command_id == 1:
                    self.send_all_rooms()
                elif command_id == 2:
                    self.subscribe(data)
                elif command_id == 3:
                    self.get_message_from_user(data)
                elif command_id == 4:
                    self.send_messages_from_room(data)

    def send_all_rooms(self):
        rooms = []
        for room_ in self.server.rooms:
            rooms.append(room_["name"])

        data = {
                "command_id": 1,
                "data": {"rooms": rooms},
                "status": "ok"
                }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def subscribe(self, data):
        room = data["data"]["room_name"]

        for room_ in self.server.rooms:
            if room_["name"] == room:
                room_["clients"].append(self.client_conn)

        data = {
            "command_id": 2,
            "status": "ok"
        }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def get_message_from_user(self, data):
        room = data["data"]["room_name"]
        message = data["data"]["message"]

        if message:
            self.server.add_message_in_room(message, room)

        data = {
            "command_id": 3,
            "status": "ok"
        }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def send_messages_from_room(self, data):
        room = data["data"]["room_name"]
        messages = []

        for room_ in self.server.rooms:
            if room == room_["name"]:
                messages = room_["messages"]
                break

        data = {"command_id": "4",
                "data": {"messages": messages}
                }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def send(self, message, room):
        data = {"command_id": "3",
                "data": {"room_name": room,
                         "message": message}
                }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)
