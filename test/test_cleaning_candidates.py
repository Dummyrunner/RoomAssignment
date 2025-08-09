import pytest
from src.person import Person
from src.room import Room
from src.room_config import RoomConfig
from src.cleaning_candidates import CleaningCandidates
import json


def test_add_person():
    candidates = CleaningCandidates()
    person = Person("John", "Doe")
    candidates.add_person(person)
    assert len(candidates.candidates) == 1
    assert candidates.candidates[0].full_name() == "John Doe"


def test_initialization_with_candidates():
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates = CleaningCandidates([person1, person2])
    assert len(candidates.candidates) == 2
    assert candidates.candidates[0].full_name() == "John Doe"
    assert candidates.candidates[1].full_name() == "Jane Smith"


def test_invalid_initialization():
    with pytest.raises(ValueError):
        CleaningCandidates(["Not a Person"])


def test_remove_person_by_full_name():
    candidates = CleaningCandidates()
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates.add_person(person1)
    candidates.add_person(person2)

    candidates.remove_person_by_full_name("John Doe")
    assert len(candidates.candidates) == 1
    assert candidates.candidates[0].full_name() == "Jane Smith"


def test_remove_person_by_name():
    candidates = CleaningCandidates()
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates.add_person(person1)
    candidates.add_person(person2)

    candidates.remove_person_by_name("Jane", "Smith")
    assert len(candidates.candidates) == 1
    assert candidates.candidates[0].full_name() == "John Doe"


def test_generate_hash():
    candidates = CleaningCandidates()
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates.add_person(person1)
    candidates.add_person(person2)

    hash1 = candidates.generate_hash()

    # Add in a different order and ensure the hash is the same
    candidates = CleaningCandidates([person2, person1])
    hash2 = candidates.generate_hash()

    assert hash1 == hash2


def test_write_to_file(tmp_path):
    candidates = CleaningCandidates()
    candidates.add_person(Person("John", "Doe"))
    candidates.add_person(Person("Jane", "Smith"))

    file_path = tmp_path / "candidates.json"
    candidates.write_to_file(file_path)

    with open(file_path, "r") as file:
        data = json.load(file)

    assert len(data) == 2
    assert data[0]["first_name"] == "John"
    assert data[0]["last_name"] == "Doe"
    assert data[1]["first_name"] == "Jane"
    assert data[1]["last_name"] == "Smith"
