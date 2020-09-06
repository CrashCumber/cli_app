import json
import pytest
from config import ROOMS
from tests.base import Base


class InvalidData:
    data1 = {
        "command_id": 3,
        "data": {"room_name": ROOMS[1]["name"],
                 "message": "message"}
    }
    data2 = {
        "command_id": 3,
        "data": {
                "nick": "test_nick",
                "message": "message"}
            }
    data3 = {
        "command_id": 3,
        "data": {
            "room_name": ROOMS[1]["name"],
            "nick": "test_nick_for_send",
            }
    }
    data4 = {
        "command_id": 3,
        "data": {
        }
    }
    data5 = {
        "command_id": 3,
        "data": {
            "room_name": "unexist room",
            "nick": "test_nick_for_send",
            "message": "message"}
    }
    data6 = {
        "command_id": 3,
        "data": {
            "room_name": ROOMS[1]["name"],
            "nick": "test_nick_for_send",
            "message": ''.join(['s' for i in range(256)])}
    }


class TestSend(Base):

    def test_send_message(self):
        room = ROOMS[1]["name"]
        num = ROOMS[1]["number"]
        nick = "test_nick_for_send"
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

        response = self.client.recv(1024).decode()
        data = json.loads(response)

        assert data.get("status") == "ok", data

        assert message in ROOMS[1]["messages"], data
        assert num+1 == ROOMS[1]["number"]

    def test_send_message_unsubscribe(self):
        room = ROOMS[1]["name"]
        nick = "unsubscribe_nick"
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

        response = self.client.recv(1024).decode()
        data = json.loads(response)

        assert data.get("status") != "ok", data
        assert message in ROOMS[1]["messages"], data

    @pytest.mark.parametrize('data', [InvalidData.data1, InvalidData.data2, InvalidData.data3, InvalidData.data4, InvalidData.data5, InvalidData.data6])
    def test_send_message_invalid_data(self, data):
        data = json.dumps(data)
        data = data.encode()

        self.client.sendall(data)

        response = self.client.recv(1024).decode()
        data = json.loads(response)

        assert data.get("status") != "ok", data
