import pytest
from src.person import Person
from src.available_persons import AvailablePersons
import json


def test_add_person():
    candidates = AvailablePersons()
    person = Person("John", "Doe")
    candidates.add_person(person)
    assert len(candidates.candidates) == 1
    assert candidates.candidates[0].full_name() == "John Doe"


def test_initialization_with_candidates():
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates = AvailablePersons([person1, person2])
    assert len(candidates.candidates) == 2
    assert candidates.candidates[0].full_name() == "John Doe"
    assert candidates.candidates[1].full_name() == "Jane Smith"


def test_invalid_initialization():
    with pytest.raises(ValueError):
        AvailablePersons(["Not a Person"])


def test_remove_person_by_full_name():
    candidates = AvailablePersons()
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates.add_person(person1)
    candidates.add_person(person2)
    candidates.remove_person_by_full_name("John Doe")
    assert len(candidates.candidates) == 1
    assert candidates.candidates[0].full_name() == "Jane Smith"


def test_remove_person_by_name():
    candidates = AvailablePersons()
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates.add_person(person1)
    candidates.add_person(person2)
    candidates.remove_person_by_name("Jane", "Smith")
    assert len(candidates.candidates) == 1
    assert candidates.candidates[0].full_name() == "John Doe"


def test_generate_hash():
    candidates = AvailablePersons()
    person1 = Person("John", "Doe")
    person2 = Person("Jane", "Smith")
    candidates.add_person(person1)
    candidates.add_person(person2)
    hash1 = candidates.generate_hash()
    candidates = AvailablePersons([person2, person1])
    hash2 = candidates.generate_hash()
    assert hash1 == hash2


def test_write_to_file(tmp_path):
    candidates = AvailablePersons()
    candidates.add_person(Person("John", "Doe"))
    candidates.add_person(Person("Jane", "Smith"))
    file_path = tmp_path / "candidates.json"
    candidates.write_to_file(file_path)
    with open(file_path, "r") as file:
        data = json.load(file)
    assert len(data) == 2 + 1
    assert data[0]["first_name"] == "John"
    assert data[0]["last_name"] == "Doe"
    assert data[1]["first_name"] == "Jane"
    assert data[1]["last_name"] == "Smith"


def test_from_csv(tmp_path):
    csv_content = """John;Doe\nJane;Smith\nAlice;Brown\n"""
    csv_path = tmp_path / "candidates.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(csv_content)
    candidates = AvailablePersons.from_csv(str(csv_path))
    assert len(candidates.candidates) == 3
    assert candidates.candidates[0].full_name() == "John Doe"
    assert candidates.candidates[1].full_name() == "Jane Smith"
    assert candidates.candidates[2].full_name() == "Alice Brown"


def test_from_csv_with_test_data():
    csv_path = "test/test_data/test_persons.csv"
    candidates = AvailablePersons.from_csv(csv_path)
    print(candidates.candidates)
    assert len(candidates.candidates) > 0
    for person in candidates.candidates:
        assert isinstance(person.first_name, str)
        assert isinstance(person.last_name, str)
        assert person.first_name != ""
        assert person.last_name != ""
