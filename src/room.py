import hashlib

class Room:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return f"Room(name={self.name}, capacity={self.capacity})"
