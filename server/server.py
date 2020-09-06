import threading
import socket
import argparse

from room_config import ROOMS
from server_client_connection import ConnSocket


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
                room_["number"] += 1
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    server = Server(args.host, args.p, rooms=ROOMS)
    server.start()
