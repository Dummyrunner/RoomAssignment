import pytest
import os
import json
from src.user_interface import UserInterface
from src.room_config import RoomConfig
from src.available_persons import AvailablePersons
from src.assignment_creator import AssignmentCreator


def test_provide_random_assignment(tmp_path):
    room_csv = tmp_path / "rooms.csv"
    person_csv = tmp_path / "persons.csv"
    with open(room_csv, "w", encoding="utf-8") as f:
        f.write("Room A;2\nRoom B;1\n")
    with open(person_csv, "w", encoding="utf-8") as f:
        f.write("John;Doe\nJane;Smith\nAlice;Brown\n")
    room_config = RoomConfig.from_csv(str(room_csv))
    available_persons = AvailablePersons.from_csv(str(person_csv))
    creator = AssignmentCreator(available_persons, room_config)
    ui = UserInterface(creator)
    assignment = ui.provide_random_assignment()
    assert assignment is not None
    # Check that all persons are assigned
    assigned = [
        person.full_name() for person, room in assignment.assignment_map.items() if room
    ]
    assert set(assigned) == {"John Doe", "Jane Smith", "Alice Brown"}


def test_used_assignments_file_creation(tmp_path):
    json_path = tmp_path / "used_assignments.json"
    room_config = RoomConfig()
    available_persons = AvailablePersons([])
    creator = AssignmentCreator(available_persons, room_config)
    ui = UserInterface(creator, used_assignments_json_path=str(json_path))
    assert os.path.exists(json_path)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data == []


def test_is_used_already(tmp_path):
    json_path = tmp_path / "used_assignments.json"
    room_csv = tmp_path / "rooms.csv"
    person_csv = tmp_path / "persons.csv"
    with open(room_csv, "w", encoding="utf-8") as f:
        f.write("Room A;2\nRoom B;1\n")
    with open(person_csv, "w", encoding="utf-8") as f:
        f.write("John;Doe\nJane;Smith\nAlice;Brown\n")
    room_config = RoomConfig.from_csv(str(room_csv))
    available_persons = AvailablePersons.from_csv(str(person_csv))
    creator = AssignmentCreator(available_persons, room_config)
    ui = UserInterface(creator, used_assignments_json_path=str(json_path))
    assignment = ui.provide_random_assignment()
    # Initially, should not be used
    assert not ui.is_used_already(assignment)
    # Add entry to JSON file
    entry = {
        "room_hash": room_config.generate_hash(),
        "candidates_hash": available_persons.generate_hash(),
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([entry], f)
    # Now should be used
    assert ui.is_used_already(assignment)
