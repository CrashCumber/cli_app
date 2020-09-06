import json
import threading
import os


class Receive(threading.Thread):
    def __init__(self, sock, name, client):
        super().__init__()
        self.sock = sock
        self.name = name
        self.client = client

    def run(self):
        while True:
            response = self.sock.recv(1024).decode()
            data = json.loads(response)

            if not data.get("status", False):
                continue

            if data.get("status") != "ok":
                print(data["status"])
                continue

            command_id = data.get("command_id")

            if command_id == 1:
                self.get_rooms_list(data)
            elif command_id == 2:
                self.subscribe(data)
            elif command_id == 3:
                pass
            elif command_id == 4:
                self.get_messages_from_room(data)
            elif command_id == 6:
                self.unsubscribe(data)
            else:
                self.sock.close()
                os._exit(0)

    def get_rooms_list(self, data):
        print('\nAll rooms:')

        rooms = data["data"]["rooms"]
        for room in rooms:
            print(room)

    def subscribe(self, data):
        room = data["data"]["room_name"]
        nick = data["data"]["nick"]
        messages = data["data"]["messages"]

        self.client.rooms[room] = nick

        print(f'You successfully subscribe on {room}')
        print(f'\nAll messages in room :')
        for message in messages:
            print(message)

    def unsubscribe(self, data):
        room = data["data"]["room_name"]

        self.client.rooms.pop(room)

        print(f'You successfully unsubscribe on {room}')

    def get_messages_from_room(self, data):
        messages = data["data"]["messages"]
        room = data["data"]["room_name"]

        print(f'\nAll messages in room {room}:')

        for message in messages:
            print(message)



