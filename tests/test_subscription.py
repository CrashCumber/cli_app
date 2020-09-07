import json
from time import sleep

from config import ROOMS
from tests.base import Base


class TestSubscription(Base):
    """
        Тестирование подписки и отписки пользователя.
    """

    def test_subscribe(self):
        room = ROOMS[1]["name"]
        nick = "test_nick_1"

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

        response = self.client.recv(1024).decode()
        data = json.loads(response)

        assert data.get("status") == "ok"
        assert data.get("data", False)

        room_ = data.get("data").get("room_name")
        assert room == room_

        messages = data.get("data").get("messages")

        assert nick in ROOMS[1]["clients"], (nick, ROOMS)
        assert messages == ROOMS[1]["messages"]

    def test_unsubscribe(self):
        room = ROOMS[1]["name"]
        nick = "test_nick_for_unsub"

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

        response = self.client.recv(1024).decode()
        data = json.loads(response)

        assert data.get("status", False) == 'ok', data
        assert data.get("data", False), data

        room_ = data.get("data").get("room_name")

        assert room == room_, (room, room_)
        assert nick not in ROOMS[1]["clients"]
