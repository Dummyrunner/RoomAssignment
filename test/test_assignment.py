import pytest
import json
from src.assignment import Assignment
from src.available_persons import AvailablePersons
from src.room_config import RoomConfig
from src.room import Room
from src.person import Person


def test_assignment_valid():
    candidates = AvailablePersons([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))
    room_config.add_room(Room("Room B", 1))

    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")
    assignment.assign(candidates.candidates[1], "Room B")

    assert assignment.valid() is True


def test_assignment_invalid_person():
    candidates = AvailablePersons([Person("John", "Doe")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))

    assignment = Assignment(candidates, room_config)
    with pytest.raises(ValueError):
        assignment.assign(Person("Jane", "Smith"), "Room A")  # Invalid person


def test_assignment_invalid_room():
    candidates = AvailablePersons([Person("John", "Doe")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))

    assignment = Assignment(candidates, room_config)
    with pytest.raises(ValueError):
        assignment.assign(candidates.candidates[0], "Invalid Room")  # Invalid room


def test_get_room_for_person():
    candidates = AvailablePersons([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))

    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")

    assert assignment.get_room_for_person(candidates.candidates[0]) == "Room A"
    assert assignment.get_room_for_person(candidates.candidates[1]) == None

    with pytest.raises(ValueError):
        assignment.get_room_for_person(Person("Nonexistent", "Person"))  # Not in map


def test_assignment_exceeds_room_capacity():
    candidates = AvailablePersons(
        [Person("John", "Doe"), Person("Jane", "Smith"), Person("Alice", "Johnson")]
    )
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))  # Capacity of 2

    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")
    assignment.assign(candidates.candidates[1], "Room A")
    assignment.assign(candidates.candidates[2], "Room A")  # Exceeds capacity

    assert assignment.valid() is False


def test_append_assignment_to_json(tmp_path):
    json_file = tmp_path / "assignments.json"
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))
    candidates = AvailablePersons([Person("John", "Doe"), Person("Jane", "Smith")])
    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")
    assignment.assign(candidates.candidates[1], "Room A")
    assignment.append_assignment_to_json(str(json_file))
    # Check file contents
    with open(json_file, "r") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) == 1
    assert {d["person"] for d in data[0]} == {"John Doe", "Jane Smith"}
    assert all(d["room"] == "Room A" for d in data[0])
    # Append again and check
    assignment.append_assignment_to_json(str(json_file))
    with open(json_file, "r") as f:
        data = json.load(f)
    assert len(data) == 2
