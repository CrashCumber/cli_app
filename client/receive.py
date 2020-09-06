import json
import threading
import os


class Receive(threading.Thread):
    """
        Поток приема сообщений с сервера.
    """
    def __init__(self, sock, name, client):
        super().__init__()
        self.sock = sock
        self.name = name
        self.client = client

    def run(self):
        """
            Прием данных с сервера.
            Перенаправление данных на необходимые методы.
        """
        while True:
            response = self.sock.recv(1024).decode()

            try:
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

            except json.decoder.JSONDecodeError:
                self.sock.close()
                os._exit(0)

    def get_rooms_list(self, data):
        """
            Вывод все доспутных на сервере комнат
        """
        print('\nAll rooms:')

        rooms = data["data"]["rooms"]
        for room in rooms:
            print(room)

    def subscribe(self, data):
        """
            Добавление комнаты и ника в словарь клиента.
        """
        room = data.get("data").get("room_name")
        nick = data.get("data").get("nick")
        messages = data["data"]["messages"]

        self.client.rooms[room] = nick

        print(f'You successfully subscribe on {room}')
        print(f'\nAll messages in room :')
        for message in messages:
            print(message)

    def unsubscribe(self, data):
        """
            Удаление комнаты и ника из словаря клиента.
        """
        room = data.get("data").get("room_name")

        self.client.rooms.pop(room)

        print(f'You successfully unsubscribe on {room}')

    def get_messages_from_room(self, data):
        """
            Вывод все сообщений из комнаты
        """
        messages = data["data"]["messages"]
        room = data.get("data").get("room_name")

        print(f'\nAll messages in room {room}:')

        for message in messages:
            print(message)



