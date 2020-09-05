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

            command_id = int(data["command_id"])

            if command_id == 1:
                self.get_all_rooms(data)
            elif command_id == 2:
                self.subscribe(data)
            elif command_id == 3:
                pass
            elif command_id == 4:
                self.get_messages_from_room(data)
            else:
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

    def get_all_rooms(self, data):
        print('\nAll rooms:\n')

        rooms = data["data"]["rooms"]
        for room in rooms:
            print(room)

    def subscribe(self, data):
        room = data["data"]["room_name"]
        self.client.rooms.append(room)

        print(f'You successfully subscribe on {room}')

    def get_messages_from_room(self, data):
        messages = data["data"]["messages"]

        print(f'\nAll messages in room :\n')

        for message in messages:
            print(message)



