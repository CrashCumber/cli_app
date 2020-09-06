import socket
import argparse
from receive import Receive
from send import Send


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.rooms = {}

    def start(self):
        self.sock.connect((self.host, self.port))
        self.name = input('Your name: ')

        send = Send(self.sock, self.name, self)
        receive = Receive(self.sock, self.name, self)

        send.start()
        receive.start()

        return receive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    client = Client(args.host, args.p)
    client.start()



# class Send(threading.Thread):
#     def __init__(self, sock, name, client):
#         super().__init__()
#         self.sock = sock
#         self.name = name
#         self.client = client
#
#     def run(self):
#         while True:
#             sleep(1)
#             print(COMMANDS)
#             command_id = int(input('Type number: '))
#
#             if command_id== 1:
#                 self.get_all_rooms()
#             elif command_id == 2:
#                 self.subscribe()
#             elif command_id ==3:
#                 self.send_message()
#             elif command_id ==4:
#                 self.get_message_from_room()
#
#         self.sock.close()
#         os._exit(0)
#
#     def get_all_rooms(self):
#         data = {"command_id": "1"}
#
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.sock.sendall(data)
#
#     def get_message_from_room(self):
#         room = input('Input room name: ')
#         data = {"command_id": "4",
#                 "data": {"room_name": room}
#                 }
#
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.sock.sendall(data)
#         self.client.rooms.append(room)
#
#     def subscribe(self):
#         room = input('Input room name: ')
#         data = {"command_id": "2",
#                 "data": {"room_name": room}
#                 }
#
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.sock.sendall(data)
#         self.client.rooms.append(room)
#
#     def send_message(self):
#         room = input('Input room name: ')
#         message = input('Message: ')
#
#         if sys.getsizeof(message) > 256:
#             print("It is too large( \n")
#             return
#
#         data = {"command_id": "3",
#                 "data": {"room_name": room,
#                          "message": message}
#                 }
#
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.sock.sendall(data)
#

# class Receive(threading.Thread):
#     def __init__(self, sock, name, client):
#         super().__init__()
#         self.sock = sock
#         self.name = name
#         self.client = client
#
#     def run(self):
#         while True:
#             message = self.sock.recv(1024).decode()
#             data = json.loads(message)
#
#             command_id = int(data["command_id"])
#             if command_id == 1:
#                 print('\nAll rooms:\n')
#                 rooms = data["data"]["rooms"]
#                 for room in rooms:
#                     print(room["name"])
#
#             elif command_id == 4:
#                 room = data["data"]["room_name"]
#                 messages = data["data"]["messages"]
#                 print(f'\nAll messages in room {room}:\n')
#                 for message in messages:
#                     print(message)
#             else:
#                 print('\nOh no, we have lost connection to the server!')
#                 print('\nQuitting...')
#                 self.sock.close()
#                 os._exit(0)
#
#
