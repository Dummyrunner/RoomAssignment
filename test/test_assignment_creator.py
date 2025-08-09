import pytest
from src.assignment_creator import AssignmentCreator
from src.cleaning_candidates import CleaningCandidates
from src.room_config import RoomConfig
from src.room import Room
from src.person import Person
from math import factorial


def test_get_valid_assignments():
    candidates = CleaningCandidates([Person("John", "Doe"), Person("Jane", "Smith")])
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 1))
    room_config.add_room(Room("Room B", 1))

    creator = AssignmentCreator(candidates, room_config)
    valid_assignments = creator.get_valid_assignments()

    # Ensure all assignments are valid
    for assignment in valid_assignments:
        assert assignment.valid()

    # Ensure the number of valid assignments matches expectations
    assert (
        len(valid_assignments) == 2
    )  # Two rooms, two candidates, one valid way to assign each


def test_get_valid_assignments_with_extra_candidates():
    candidates = CleaningCandidates(
        [Person("John", "Doe"), Person("Jane", "Smith"), Person("Alice", "Johnson")]
    )
    room_config = RoomConfig()
    room_config.add_room(Room("Room A", 1))
    room_config.add_room(Room("Room B", 1))  # Total capacity = 2

    creator = AssignmentCreator(candidates, room_config)
    valid_assignments = creator.get_valid_assignments()

    # Ensure all assignments are valid
    for assignment in valid_assignments:
        assert assignment.valid()

    # Ensure the number of valid assignments matches expectations
    # 3 candidates, 2 rooms, 1 "None" (unassigned) -> permutations of 3 items
    assert len(valid_assignments) == factorial(3)  # 3! = 6 permutations


def test_get_valid_assignments_with_two_extra_candidates():
    candidates = CleaningCandidates(
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
    valid_assignments = creator.get_valid_assignments()

    # Ensure all assignments are valid
    for assignment in valid_assignments:
        assert assignment.valid()

    # Ensure the number of valid assignments matches expectations
    # 4 candidates, 2 rooms, 2 "None" (unassigned) -> permutations of 4 items
    assert len(valid_assignments) == factorial(4)  # 4! = 24 permutations
