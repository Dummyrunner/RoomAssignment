from src.cleaning_candidates import AvailablePersons
from src.room_config import RoomConfig
from src.assignment_creator import AssignmentCreator
from src.user_interface import UserInterface


def main():
    room_config = RoomConfig.from_csv("data/test_rooms.csv")
    candidates = AvailablePersons.from_csv("data/test_persons.csv")

    print("---------")
    print(room_config)
    print("---------")
    print(candidates)
    print("---------")
    print("Room configuration hash:", room_config.generate_hash())
    print("Candidates hash:", candidates.generate_hash())
    print("---------")
    assignment_creator = AssignmentCreator(candidates, room_config)
    # all_valid_assignments = assignment_creator.get_all_valid_assignments()
    # print(all_valid_assignments)
    # print(f"Number of valid assignments: {len(all_valid_assignments)}")
    user_interface = UserInterface(assignment_creator)
    rnd_assignment = user_interface.provide_random_assignment()
    print(
        f"Random assignment: {rnd_assignment}\n Used: {user_interface.is_used_already(rnd_assignment)}"
    )
    rnd_assignment.append_assignment_to_json(user_interface.assignments_json_path)
    with open(user_interface.assignments_json_path, "r") as f:
        print(f.read())


if __name__ == "__main__":
    main()
