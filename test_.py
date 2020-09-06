import json
import os
import sys
from time import sleep

import pytest
import requests

from server.room_config import ROOMS


class TestServer:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config):
        self.client = config

    def test_get_list_rooms(self):
        data = {
           "command_id": 1
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.send(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") == "ok"

        assert data.get("data", False)
        rooms = data.get("data").get("rooms")

        rooms_ = []
        for room in ROOMS:
            rooms_.append(room["name"])

        assert rooms == rooms_

    def test_subscribe(self):
        room = ROOMS[1]["name"]
        nick = "test_nick"

        data = {
            "command_id": 2,
            "data": {
                "room_name": room,
                "nick": nick
            }
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") == "ok"

        assert data.get("data", False)
        assert room == data.get("data").get("room_name")

        messages = data.get("data").get("messages")
        room = data.get("data").get("room_name")

        for room_ in ROOMS:
            if room_["name"] == room:
                assert nick in room_["clients"]
                assert messages == room_["messages"]
                return

        assert False

    @pytest.mark.skip()
    def test_unsubscribe(self):
        room = ROOMS[1]["name"]
        nick = "test_nick"

        data = {
            "command_id": 6,
            "data": {
                "room_name": room,
                "nick": nick
            }
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") == "ok"

        assert data.get("data", False)
        assert room == data.get("data").get("room_name")

        room = data.get("data").get("room_name")

        for room_ in ROOMS:
            if room_["name"] == room:
                assert nick not in room_["clients"]

    def test_send_message(self):
        room = ROOMS[1]["name"]
        num = ROOMS[1]["number"]
        nick = "test_nick"
        message = "message from user"

        data = {
            "command_id": 3,
            "data": {"room_name": room,
                     "nick": nick,
                     "message": message}
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") == "ok", data

        assert message in ROOMS[1]["messages"], data
        assert num+1 == ROOMS[1]["number"]

    def test_send_message_unsubscribe(self):
        room = ROOMS[1]["name"]
        nick = "unsub_nick"
        message = "message from user"

        data = {
            "command_id": 3,
            "data": {"room_name": room,
                     "nick": nick,
                     "message": message}
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") != "ok", data

        assert message in ROOMS[1]["messages"], data

    def test_get_message(self):
        room = ROOMS[1]["name"]
        nick = "test_nick"

        data = {
            "command_id": 4,
            "data": {"room_name": room,
                     "nick": nick
                     }
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") == "ok", data

        assert data.get("data").get("messages") == ROOMS[1]["messages"], data

    def test_get_message_unsubscribe(self):
        room = ROOMS[1]["name"]
        nick = "unsub_nick"

        data = {
            "command_id": 4,
            "data": {"room_name": room,
                     "nick": nick
                     }
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") != "ok", data

        assert not data.get("data").get("messages", False)

