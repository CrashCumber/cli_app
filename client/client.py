import socket
from receive import Receive
from send import Send


class Client:
    """
        Клиент соединения
        Содержит информацию о соственных комнатах.
        Понимается на 127.0.0.1:1060
        Создание сокета клиента.
        Запуск потоков на отправку и чтение.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.rooms = {}

    def start(self):
        """
        Создание сокета клиента.
        Подключение к серверу.
        Запуск потоков на отправку и чтение.
        """
        self.sock.connect((self.host, self.port))
        self.name = input('Your name: ')

        send = Send(self.sock, self.name, self)
        receive = Receive(self.sock, self.name, self)

        send.start()
        receive.start()

        return receive


if __name__ == '__main__':

    client = Client('127.0.0.1', 1060)
    client.start()
