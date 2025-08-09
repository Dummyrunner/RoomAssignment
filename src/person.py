class Person:
    def __init__(self, first_name: str, last_name: str):
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name must be a non-empty string.")
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name must be a non-empty string.")

        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"Person(first_name={self.first_name}, last_name={self.last_name})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
