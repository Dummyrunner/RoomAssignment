from src.person import Person
import json
import hashlib
import csv


class AvailablePersons:
    def __init__(self, candidates=None):
        if candidates is None:
            self.candidates = []
        else:
            if not all(isinstance(person, Person) for person in candidates):
                raise ValueError("All elements must be Person objects.")
            self.candidates = candidates

    def add_person(self, person: Person):
        if not isinstance(person, Person):
            raise ValueError("Only Person objects can be added.")
        self.candidates.append(person)

    def remove_person_by_full_name(self, full_name: str):
        self.candidates = [
            person for person in self.candidates if person.full_name() != full_name
        ]

    def remove_person_by_name(self, first_name: str, last_name: str):
        self.candidates = [
            person
            for person in self.candidates
            if person.first_name != first_name or person.last_name != last_name
        ]

    def generate_hash(self):
        # Sort candidates by full name to ensure order independence
        candidate_data = sorted(person.full_name() for person in self.candidates)
        candidate_data_str = json.dumps(candidate_data, sort_keys=True)
        return hashlib.sha256(candidate_data_str.encode()).hexdigest()

    def write_to_file(self, filepath: str):
        candidate_data = [
            {"first_name": person.first_name, "last_name": person.last_name}
            for person in self.candidates
        ]
        candidate_data.append({"hash": self.generate_hash()})
        with open(filepath, "w") as file:
            json.dump(candidate_data, file, indent=4)

    @staticmethod
    def from_csv(filepath: str):
        """Factory method to create AvailablePersons from a CSV file."""
        candidates = AvailablePersons()
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            for row in reader:
                if len(row) < 2:
                    continue  # skip invalid rows
                first_name, last_name = row[0], row[1]
                try:
                    person = Person(first_name, last_name)
                except ValueError:
                    continue  # skip invalid person data
                candidates.add_person(person)
        return candidates

    def __iter__(self):
        return iter(self.candidates)

    def __str__(self):
        person_list = [f"{person.full_name()}" for person in self.candidates]
        return "AvailablePersons: [" + ", ".join(person_list) + "]"
