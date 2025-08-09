import pytest
from src.assignment import Assignment
from src.cleaning_candidates import CleaningCandidates
from src.room_config import RoomConfig
from src.room import Room
from src.person import Person


def test_assignment_valid():
    candidates = CleaningCandidates([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))
    room_config.add_room(Room("Room B", 1))

    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")
    assignment.assign(candidates.candidates[1], "Room B")

    assert assignment.valid() is True


def test_assignment_invalid_person():
    candidates = CleaningCandidates([Person("John", "Doe")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))

    assignment = Assignment(candidates, room_config)
    with pytest.raises(ValueError):
        assignment.assign(Person("Jane", "Smith"), "Room A")  # Invalid person


def test_assignment_invalid_room():
    candidates = CleaningCandidates([Person("John", "Doe")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))

    assignment = Assignment(candidates, room_config)
    with pytest.raises(ValueError):
        assignment.assign(candidates.candidates[0], "Invalid Room")  # Invalid room


def test_get_room_for_person():
    candidates = CleaningCandidates([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))

    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")

    assert assignment.get_room_for_person(candidates.candidates[0]) == "Room A"
    assert assignment.get_room_for_person(candidates.candidates[1]) == None

    with pytest.raises(ValueError):
        assignment.get_room_for_person(Person("Nonexistent", "Person"))  # Not in map


def test_assignment_exceeds_room_capacity():
    candidates = CleaningCandidates(
        [Person("John", "Doe"), Person("Jane", "Smith"), Person("Alice", "Johnson")]
    )
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 2))  # Capacity of 2

    assignment = Assignment(candidates, room_config)
    assignment.assign(candidates.candidates[0], "Room A")
    assignment.assign(candidates.candidates[1], "Room A")
    assignment.assign(candidates.candidates[2], "Room A")  # Exceeds capacity

    assert assignment.valid() is False
