from itertools import permutations
import random
from src.assignment import Assignment
from src.available_persons import AvailablePersons
from src.room_config import RoomConfig
from src.person import Person


class AssignmentCreator:
    def __init__(self, cleaning_candidates: AvailablePersons, room_config: RoomConfig):
        self.cleaning_candidates = cleaning_candidates
        self.room_config = room_config

    def get_all_valid_assignments(self):
        from itertools import permutations

        valid_assignments = []
        candidates = self.cleaning_candidates.candidates
        rooms = self.room_config.rooms
        room_slots = []
        for room in rooms:
            room_slots.extend([room.name] * room.capacity)
        # If there are more candidates than slots, raise an error
        if len(candidates) > len(room_slots):
            raise ValueError("Not enough room slots for all candidates.")
        # Add None slots for unassigned candidates (not needed anymore)
        slots = room_slots
        for perm in set(permutations(slots, len(candidates))):
            assignment = Assignment(self.cleaning_candidates, self.room_config)
            for person, room_name in zip(candidates, perm):
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
