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

                if not data.get("command_id", False):
                    data = {"status": "Invalid request data"}
                    data = json.dumps(data)
                    data = data.encode()

                    self.client_conn.sendall(data)
                    continue

                command_id = data["command_id"]

                if command_id == 1:
                    self.send_rooms_list()
                elif command_id == 2:
                    self.subscribe(data)
                elif command_id == 3:
                    self.send_message_in_room(data)
                elif command_id == 4:
                    self.get_messages_from_room(data)
                elif command_id == 6:
                    self.unsubscribe(data)

    def send_rooms_list(self):
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
        room = data.get("data").get("room_name")
        nick = data.get("data").get("nick")
        messages = []
        status = "Invalid request data"

        for room_ in self.server.rooms:
            if room_["name"] == room:
                if nick in room_["clients"]:
                    status = "User with this nick has already had in room"
                    break
                else:
                    room_["clients"].append(nick)
                    messages = room_["messages"]
                    status = "ok"
                    break

        data = {
            "command_id": 2,
            "data": {"room_name": room,
                     "nick": nick,
                     "messages": messages},
            "status": status
        }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def unsubscribe(self, data):
        room = data.get("data").get("room_name")
        nick = data.get("data").get("nick")
        status = "Invalid request data"

        for room_ in self.server.rooms:
            if room_["name"] == room:
                room_["clients"].remove(nick)
                status = "ok"
                break

        data = {
            "command_id": 6,
            "data": {"room_name": room},
            "status": status
        }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def send_message_in_room(self, data):
        room = data.get("data").get("room_name")
        nick = data.get("data").get("nick")
        message = data.get("data").get("message")

        status = "Invalid request data"

        if message:
            for room_ in self.server.rooms:
                if room == room_["name"]:
                    if nick in room_["clients"]:
                        if room_["number"] >= 128:
                            status = 'In room a lot of messages. You can`t add more.'
                            break
                        room_["messages"].append(message)
                        room_["number"] += 1
                        status = "ok"
                    else:
                        status = "You unsubscribe on this room"
                    break

        data = {
            "command_id": 3,
            "status": status
        }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)

    def get_messages_from_room(self, data):
        room = data.get("data").get("room_name")
        nick = data.get("data").get("nick")
        messages = []
        status = "Invalid request data"

        for room_ in self.server.rooms:
            if room == room_["name"]:
                if nick in room_["clients"]:
                    messages = room_["messages"]
                    status = "ok"
                else:
                    status = "You unsubscribe on this room"
                break


        data = {"command_id": 4,
                "data": {
                         "room_name": room,
                         "messages": messages
                        },
                "status": status
                }

        data = json.dumps(data)
        data = data.encode()

        self.client_conn.sendall(data)
