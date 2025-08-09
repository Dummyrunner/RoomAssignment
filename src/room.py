import hashlib


class Room:
    def __init__(self, name: str, capacity: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Room name must be a non-empty string.")
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Room capacity must be an integer greater than zero.")
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return f"Room(name={self.name}, capacity={self.capacity})"
