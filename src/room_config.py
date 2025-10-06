import json
import hashlib
import csv
from src.room import Room


class RoomConfig:
    def __init__(self):
        self.rooms = []

    def add_room(self, room: Room):
        if not isinstance(room, Room):
            raise ValueError("Only Room objects can be added.")
        self.rooms.append(room)

    def remove_room(self, name: str):
        self.rooms = [room for room in self.rooms if room.name != name]

    def generate_hash(self):
        # Sort room data by name and capacity to ensure order independence
        room_data = sorted((room.name, room.capacity) for room in self.rooms)
        room_data_str = json.dumps(room_data, sort_keys=True)
        return hashlib.sha256(room_data_str.encode()).hexdigest()

    def save_to_file(self, filepath: str):
        room_data = [
            {"name": room.name, "capacity": room.capacity} for room in self.rooms
        ]
        with open(filepath, "w") as file:
            json.dump(room_data, file, indent=4)

    def read_from_dict(self, data: list):
        self.rooms = [Room(item["name"], item["capacity"]) for item in data]

    def read_from_file(self, filepath: str):
        with open(filepath, "r") as file:
            data = json.load(file)
        self.read_from_dict(data)

    def write_to_file(self, filepath: str):
        room_data = [
            {"name": room.name, "capacity": room.capacity} for room in self.rooms
        ]
        room_data.append({"hash": self.generate_hash()})
        with open(filepath, "w") as file:
            json.dump(room_data, file, indent=4)

    @staticmethod
    def from_csv(filepath: str):
        """Factory method to create RoomConfig from a CSV file with ';' as separator."""
        config = RoomConfig()
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            for row in reader:
                if len(row) < 2:
                    continue  # skip invalid rows
                name, capacity = row[0], row[1]
                try:
                    capacity = int(capacity)
                except ValueError:
                    continue  # skip rows with invalid capacity
                config.add_room(Room(name, capacity))
        return config

    def __str__(self):
        room_list = [f"{room.name}: {room.capacity}" for room in self.rooms]
        return "RoomConfig: [" + ", ".join(room_list) + "]"
