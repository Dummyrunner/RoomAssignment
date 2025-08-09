from src.room import Room
from src.room_config import RoomConfig

def main():
    config = RoomConfig()
    config.add_room(Room("Conference Room", 10))
    config.add_room(Room("Meeting Room", 5))

    print("Room configuration hash:", config.generate_hash())
    config.save_to_file("data/room_config.json")

if __name__ == "__main__":
    main()
