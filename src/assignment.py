from src.cleaning_candidates import CleaningCandidates
from src.room_config import RoomConfig
from src.person import Person


class Assignment:
    def __init__(
        self, cleaning_candidates: CleaningCandidates, room_config: RoomConfig
    ):
        self.cleaning_candidates = cleaning_candidates
        self.room_config = room_config
        self.assignment_map = {}

        # Initialize all persons as unassigned
        for person in cleaning_candidates:
            self.assignment_map[person] = None

    def assign(self, person: Person, room_name: str):
        if room_name not in [room.name for room in self.room_config.rooms]:
            raise ValueError(f"Room '{room_name}' does not exist in the room config.")
        if person not in self.cleaning_candidates.candidates:
            raise ValueError(
                f"Person '{person.full_name()}' is not in cleaning candidates."
            )
        self.assignment_map[person] = room_name

    def get_room_for_person(self, person: Person) -> str:
        if person not in self.assignment_map:
            raise ValueError(
                f"Person '{person.full_name()}' is not in the assignment map."
            )
        return self.assignment_map[person]

    def valid(self) -> bool:
        # Check that all persons in the assignment map are in cleaning candidates
        if not all(
            person in self.cleaning_candidates.candidates
            for person in self.assignment_map.keys()
        ):
            return False

        # Check that all rooms in the assignment map are in the room config
        valid_rooms = {room.name for room in self.room_config.rooms}
        if not all(
            room in valid_rooms for room in self.assignment_map.values() if room
        ):
            return False

        # Check that the number of persons assigned to a room does not exceed its capacity
        room_capacity = {room.name: room.capacity for room in self.room_config.rooms}
        room_assignments = {room: 0 for room in valid_rooms}
        for room in self.assignment_map.values():
            if room:
                room_assignments[room] += 1

        if any(
            room_assignments[room] > room_capacity[room] for room in room_assignments
        ):
            return False

        return True
