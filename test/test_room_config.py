import os
import pytest
import json
from src.room import Room
from src.room_config import RoomConfig


def test_add_room():
    config = RoomConfig()
    room = Room(name="Conference Room", capacity=10)
    config.add_room(room)
    assert len(config.rooms) == 1
    assert config.rooms[0].name == "Conference Room"


def test_generate_hash():
    config = RoomConfig()
    room = Room(name="Conference Room", capacity=10)
    config.add_room(room)
    room_hash = config.generate_hash()
    assert isinstance(room_hash, str)
    assert len(room_hash) == 64  # SHA-256 hash length


def test_save_to_file(tmp_path):
    config = RoomConfig()
    config.add_room(Room("Room A", 10))
    config.add_room(Room("Room B", 5))

    file_path = tmp_path / "room_config.json"
    config.save_to_file(file_path)

    assert os.path.exists(file_path)
    with open(file_path, "r") as file:
        data = file.read()
        assert '"name": "Room A"' in data
        assert '"capacity": 10' in data


def test_room_config_hash_order_independence():
    config1 = RoomConfig()
    config1.add_room(Room("Room A", 10))
    config1.add_room(Room("Room B", 5))

    config2 = RoomConfig()
    config2.add_room(Room("Room B", 5))
    config2.add_room(Room("Room A", 10))

    assert config1.generate_hash() == config2.generate_hash()


def test_remove_room():
    config = RoomConfig()
    config.add_room(Room("Room A", 10))
    config.add_room(Room("Room B", 5))
    config.remove_room("Room A")
    assert len(config.rooms) == 1
    assert config.rooms[0].name == "Room B"


def test_read_from_dict():
    config = RoomConfig()
    data = [{"name": "Room A", "capacity": 10}, {"name": "Room B", "capacity": 5}]
    config.read_from_dict(data)
    assert len(config.rooms) == 2
    assert config.rooms[0].name == "Room A"
    assert config.rooms[1].capacity == 5


def test_read_from_file(tmp_path):
    config = RoomConfig()
    data = [{"name": "Room A", "capacity": 10}, {"name": "Room B", "capacity": 5}]
    file_path = tmp_path / "room_config.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    config.read_from_file(file_path)
    assert len(config.rooms) == 2
    assert config.rooms[0].name == "Room A"
    assert config.rooms[1].capacity == 5
