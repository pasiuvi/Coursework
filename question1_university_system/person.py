class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def get_responsibilities(self):
        return "General responsibilities"


class Staff(Person):
    def get_responsibilities(self):
        return "Administrative duties"
