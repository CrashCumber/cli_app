import threading
import socket
import argparse
from server_client_connection import ConnSocket


ROOMS = [
    {
        "name": "gym",
        "clients": [],
        "messages": [],
        "number": 0
     },
    {
        "name": "cinema",
        "clients": [],
        "messages": [],
        "number": 0
    },
    {
        "name": "school",
        "clients": [],
        "messages": [],
        "number": 0
    },
]


class Server(threading.Thread):

    def __init__(self, host, port, rooms):
        super().__init__()
        self.host = host
        self.port = port
        self.client_connections = []
        self.rooms = rooms

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)

        while True:
            client_conn, addr = sock.accept()

            client_conn_socket = ConnSocket(client_conn, addr, self)
            client_conn_socket.start()

            self.client_connections.append(client_conn_socket)

    def add_message_in_room(self, message, room):

        for room_ in self.rooms:
            if room == room_["name"]:
                room_["messages"].append(message)
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    server = Server(args.host, args.p, rooms=ROOMS)
    server.start()




       # for connection in clients:
        #     if connection.sockname != source:
        #         connection.send(message, room)


# class ConnSocket(threading.Thread):
#     def __init__(self, client_conn, addr, server):
#         super().__init__()
#         self.client_conn = client_conn
#         self.addr = addr
#         self.server = server
#
#     def run(self):
#         while True:
#             data = self.client_conn.recv(1024).decode()
#             print(data)
#             if data:
#                 data = json.loads(data)
#                 command_id = int(data["command_id"])
#
#                 print(command_id)
#                 if command_id == 3:
#                     self.get_message(data)
#                 elif command_id == 1:
#                     self.send_all_rooms()
#                 elif command_id == 2:
#                     self.subscribe(data)
#                 elif command_id == 4:
#                     self.send_message_from_room(data)
#
#     def send_all_rooms(self):
#         data = {"command_id": 1,
#                 "data": {"rooms": self.server.rooms},
#                 "status": "ok"
#                 }
#
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.client_conn.sendall(data)
#
#     def subscribe(self, data):
#         room = data["data"]["room_name"]
#         for room_ in self.server.rooms:
#             if room_["name"] == room:
#                 room_["clients"].append(self.client_conn)
#
#     def get_message(self, data):
#         room = data["data"]["room_name"]
#         message = data["data"]["message"]
#
#         if message:
#             print('{} says {!r}'.format(self.addr, message))
#             self.server.add_message_in_room(message, self.addr, room)
#
#     def send_message_from_room(self, data):
#         room = data["data"]["room_name"]
#         messages = [
#         ]
#
#         for room_ in self.server.rooms:
#             if room == room_["name"]:
#                 messages = room_["messages"]
#
#         data = {"command_id": "4",
#                 "data": {"room_name": room,
#                          "messages": messages}
#                 }
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.client_conn.sendall(data)
#
#     def send(self, message, room):
#         data = {"command_id": "3",
#                 "data": {"room_name": room,
#                          "message": message}
#                 }
#
#         data = json.dumps(data)
#         data = data.encode()
#
#         self.client_conn.sendall(data)

