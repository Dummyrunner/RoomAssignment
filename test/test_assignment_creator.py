import pytest
from src.assignment_creator import AssignmentCreator
from src.available_persons import AvailablePersons
from src.room_config import RoomConfig
from src.room import Room
from src.person import Person
from math import factorial
from src.assignment import Assignment


def test_get_valid_assignments():
    candidates = AvailablePersons([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 1))
    room_config.add_room(Room("Room B", 1))

    creator = AssignmentCreator(candidates, room_config)
    valid_assignments = creator.get_all_valid_assignments()

    # Ensure all assignments are valid
    for assignment in valid_assignments:
        assert assignment.valid()

    # Ensure the number of valid assignments matches expectations
    assert (
        len(valid_assignments) == 2
    )  # Two rooms, two candidates, one valid way to assign each


def test_get_valid_assignments_with_extra_candidates():
    candidates = AvailablePersons(
        [Person("John", "Doe"), Person("Jane", "Smith"), Person("Alice", "Johnson")]
    )
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 1))
    room_config.add_room(Room("Room B", 1))  # Total capacity = 2

    creator = AssignmentCreator(candidates, room_config)
    with pytest.raises(ValueError):
        creator.get_all_valid_assignments()


def test_get_valid_assignments_with_two_extra_candidates():
    candidates = AvailablePersons(
        [
            Person("John", "Doe"),
            Person("Jane", "Smith"),
            Person("Alice", "Johnson"),
            Person("Bob", "Brown"),
        ]
    )
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 1))
    room_config.add_room(Room("Room B", 1))  # Total capacity = 2

    creator = AssignmentCreator(candidates, room_config)
    with pytest.raises(ValueError):
        creator.get_all_valid_assignments()


def test_get_random_valid_assignment():
    candidates = AvailablePersons([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 1))
    room_config.add_room(Room("Room B", 1))

    creator = AssignmentCreator(candidates, room_config)
    random_assignment = creator.get_random_valid_assignment()

    # Ensure the random assignment is valid
    assert random_assignment is not None
    assert isinstance(random_assignment, Assignment)
    assert random_assignment.valid()
