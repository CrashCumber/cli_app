import os
import socket
from time import sleep

import pytest
import requests

from server.room_config import ROOMS
from server.server import Server


@pytest.fixture(scope='session')
def config():
    host = "localhost"
    port = 1060

    server = Server(host, port, rooms=ROOMS)
    server.start()

    sleep(1)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((host, port))

    yield client

    os._exit(0)
