import json
import threading
import os
import sys
from time import sleep

COMMANDS = """
1. Get all rooms
2. Subscribe
3. Send message
4. Get all message one room
8. Exit
"""


class Send(threading.Thread):
    def __init__(self, sock, name, client):
        super().__init__()
        self.sock = sock
        self.name = name
        self.client = client

    def run(self):
        while True:
            sleep(1)
            print(COMMANDS)
            command_id = input('Type number: ')

            if int(command_id) == 1:
                self.get_all_rooms()
            elif int(command_id) == 2:
                self.subscribe()
            elif int(command_id) == 3:
                self.send_message_in_room()
            elif int(command_id) == 4:
                self.get_message_from_room()
            elif int(command_id) == 8:
                self.sock.close()
                os._exit(0)
            else:
                print('You enter something strange:( \n Try again')

    def get_all_rooms(self):
        data = {"command_id": "1"}

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def get_message_from_room(self):
        room = input('Input room name: ')

        data = {
                "command_id": "4",
                "data": {"room_name": room}
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def subscribe(self):
        room = input('Input room name: ')

        data = {
                "command_id": "2",
                "data": {"room_name": room}
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def send_message_in_room(self):
        room = input('Input room name: ')
        message = input('Message: ')

        if sys.getsizeof(message) > 256:
            print("It is too large( \n")
            return

        data = {"command_id": "3",
                "data": {"room_name": room,
                         "message": message}
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

