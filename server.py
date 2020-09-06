import json
import os
import threading
import socket
from config import ROOMS


class Server(threading.Thread):
    """
        Сервер, управляющей всеми соединениями.
        Содержит информацию о комнатах.
        Понимается на 127.0.0.1:1060
    """

    def __init__(self, host, port, rooms):
        super().__init__()
        self.host = host
        self.port = port
        self.client_connections = []
        self.rooms = rooms

    def run(self):
        """
            Создание сокета сервера.
            Полключение сокета в хосту и порту.
            Прослушка соединений клиента и запуск каджого клиента в новом потоке.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)

        while True:
            client_conn, addr = sock.accept()

            client_conn_socket = BindClient(client_conn, addr, self)
            client_conn_socket.start()

            self.client_connections.append(client_conn_socket)

    def add_message_in_room(self, message, room):
        """
            Добавление сообщения от клиента в информацию о камнатах
        """

        for room_ in self.rooms:
            if room == room_["name"]:
                room_["messages"].append(message)
                room_["number"] += 1
                break


class BindClient(threading.Thread):
    """
        Коммуникация с каждым отдельным клиентам.
        Прием и управление запросами пользователя.
    """

    def __init__(self, client_conn, addr, server):
        super().__init__()
        self.client_conn = client_conn
        self.addr = addr
        self.server = server

    def run(self):
        """
            Получение запросов пользователя.
            Управление запросами пользователя и перенаправление команд на необходимые действия сервера.
        """
        while True:
            request = self.client_conn.recv(1024).decode()

            if request:
                data = json.loads(request)

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
        """
            Отправка списка всех комнат, доступных на сервере.
            :return: {
                        "command_id": 1,
                        "data": {"rooms": rooms},
                        "status": "ok"  or definition of error
                        }
        """
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
        """
            Добавление пользователя в определенную комнату
        :param data:   {
                        "command_id" : 2,
                        "data" : {"room_name": "..."
                                  "nick": "..."}
                        }
        :return:    {
                        "command_id": 2,
                        "data": {
                                "room_name": "..",
                                "nick": "...",
                                "messages": [..]
                                },
                        "status": "ok" or definition of error
                    }
        """
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
        """
            Удаление пользователя из комнаты
        :param data:   {
                        "command_id" : 2,
                        "data" : {"room_name": "...",
                                  "nick": "..."}
                        }
        :return:    {
                        "command_id": 2,
                        "data": {
                                "room_name": ".."
                                },
                        "status": "ok" or definition of error
                    }
        """
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
        """
            Отправка сообщения  пользователя в определенную комнату
        :param data:   {
                        "command_id" : 2,
                        "data" : {"room_name": "..."
                                  "nick": "...",
                                  "messages": "..."}
                        }
        :return:    {
                        "command_id": 2,
                        "status": "ok" or definition of error
                    }
        """
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
        """
            Получение сообщениц отпредененной комнаты
        :param data:   {
                        "command_id" : 2,
                        "data" : {"room_name": "..."
                                  "nick": "..."}
                        }
        :return:    {
                        "command_id": 2,
                        "data": {
                                "room_name": "..",
                                "messages": [..]
                                },
                        "status": "ok" or definition of error
                    }
        """

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


def exit(server):
    """
        Остановить сервер и прекратить все соединения пользователей.
    """
    while True:
        ipt = input('')
        if ipt == 'q':
            print('Close all connections')
            for connection in server.client_connections:
                connection.client_conn.close()
            print('Shut down the server')
            os._exit(0)


if __name__ == '__main__':
    server = Server('127.0.0.1', 1060, rooms=ROOMS)
    server.start()

    exit = threading.Thread(target=exit, args=(server,))
    exit.start()
