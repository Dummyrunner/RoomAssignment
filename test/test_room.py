import pytest
from src.room import Room

def test_room_creation():
    room = Room("Test Room", 10)
    assert room.name == "Test Room"
    assert room.capacity == 10

def test_invalid_room_name():
    with pytest.raises(ValueError):
        Room("", 10)

def test_invalid_room_capacity():
    with pytest.raises(ValueError):
        Room("Test Room", 0)
    with pytest.raises(ValueError):
        Room("Test Room", -5)
