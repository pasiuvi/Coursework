from person import Person

class Faculty(Person):
    def __init__(self, name, id, department):
        super().__init__(name, id)
        self.department = department

    def get_responsibilities(self):
        return "Teach and research"

    def calculate_workload(self):
        return "Standard workload"


class Professor(Faculty):
    def calculate_workload(self):
        return "High workload with research"


class Lecturer(Faculty):
    def calculate_workload(self):
        return "Teaching focused"


class TA(Faculty):
    def calculate_workload(self):
        return "Assist in teaching"
