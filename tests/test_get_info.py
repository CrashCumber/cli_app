import json
import pytest
from config import ROOMS
from tests.base import Base


class InvalidData:
    data1 = {
        "command_id": 4,
        "data": {"room_name": "",
                 "nick": "test_nick"
                 }
    }
    data2 = {
        "command_id": 4,
        "data": {"room_name": ROOMS[1]["name"],
                 }
    }
    data3 = {
        "command_id": 4,
        "data": {}
    }
    data4 = {
    }


class TestGetInformation(Base):

    def test_get_list_rooms(self):
        data = {"command_id": 1}

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

    def test_get_messages(self):
        room = ROOMS[1]["name"]
        nick = "test_nick_for_get"

        # self.subscribe(room, nick)

        data = {
            "command_id": 4,
            "data": {"room_name": room,
                     "nick": nick
                     }
        }

        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(1024).decode()
        data = json.loads(response)

        assert data.get("status") == "ok", data
        assert data.get("data").get("messages") == ROOMS[1]["messages"], data

    def test_get_message_unsubscribe_user(self):
        room = ROOMS[1]["name"]
        nick = "unsubscribe_nick"

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
        assert data.get("data").get("messages", False) == []

    @pytest.mark.parametrize('data', [InvalidData.data1, InvalidData.data2, InvalidData.data3, InvalidData.data4])
    def test_get_message_invalid_data(self, data):
        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(5000).decode()
        data = json.loads(response)

        assert data.get("status") != "ok", data
