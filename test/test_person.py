import pytest
from src.person import Person


def test_person_creation():
    person = Person("John", "Doe")
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.full_name() == "John Doe"


def test_invalid_first_name():
    with pytest.raises(ValueError):
        Person("", "Doe")
    with pytest.raises(ValueError):
        Person(None, "Doe")


def test_invalid_last_name():
    with pytest.raises(ValueError):
        Person("John", "")
    with pytest.raises(ValueError):
        Person("John", None)
