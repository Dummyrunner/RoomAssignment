import os
import json
from src.assignment_creator import AssignmentCreator
from src.available_persons import AvailablePersons
from src.assignment import Assignment


class UserInterface:
    def __init__(
        self,
        assignment_creator: AssignmentCreator,
        used_assignments_json_path="data/used_assignments.json",
    ):
        self.assignment_creator = assignment_creator
        self.assignments_json_path = used_assignments_json_path
        # Ensure the file exists
        if not os.path.exists(self.assignments_json_path):
            os.makedirs(os.path.dirname(self.assignments_json_path), exist_ok=True)
            with open(self.assignments_json_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def set_rooms(self, room_config):
        self.assignment_creator.room_config = room_config

    def get_rooms(self):
        return self.assignment_creator.room_config

    def set_candidates(self, available_persons: AvailablePersons):
        self.assignment_creator.cleaning_candidates = available_persons

    def get_candidates(self):
        return self.assignment_creator.cleaning_candidates

    def provide_random_assignment(self) -> Assignment:
        assignment = self.assignment_creator.get_random_valid_assignment()
        return assignment

    def is_used_already(self, assignment) -> bool:
        # ATTACK HERE

        # Load used assignments from JSON file
        try:
            with open(self.assignments_json_path, "r", encoding="utf-8") as f:
                used_assignments = json.load(f)
        except Exception:
            raise RuntimeError("File loading failed.")
        # Get current hashes
        room_hash = self.assignment_creator.room_config.generate_hash()
        candidates_hash = self.assignment_creator.cleaning_candidates.generate_hash()
        # Check for matching entry
        for entry in used_assignments:
            if (
                entry.get("room_hash") == room_hash
                and entry.get("candidates_hash") == candidates_hash
            ):
                return True
        return False
