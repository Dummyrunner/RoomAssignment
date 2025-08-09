from itertools import permutations
import random
from src.assignment import Assignment
from src.cleaning_candidates import CleaningCandidates
from src.room_config import RoomConfig
from src.person import Person


class AssignmentCreator:
    def __init__(
        self, cleaning_candidates: CleaningCandidates, room_config: RoomConfig
    ):
        self.cleaning_candidates = cleaning_candidates
        self.room_config = room_config

    def get_all_valid_assignments(self):
        valid_assignments = []
        room_names = [room.name for room in self.room_config.rooms]

        # Generate all possible assignments of candidates to rooms
        for perm in permutations(
            room_names
            + [None] * (len(self.cleaning_candidates.candidates) - len(room_names))
        ):
            assignment = Assignment(self.cleaning_candidates, self.room_config)
            for person, room_name in zip(self.cleaning_candidates.candidates, perm):
                if room_name:
                    assignment.assign(person, room_name)
            if assignment.valid():
                valid_assignments.append(assignment)

        return valid_assignments

    def get_random_valid_assignment(self):
        all_assignments = self.get_all_valid_assignments()
        if not all_assignments:
            return None
        return random.choice(all_assignments)
