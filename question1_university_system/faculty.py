from person import Person

class Faculty(Person):
    """A class to represent a faculty member, inheriting from Person."""

    def __init__(self, name, age, faculty_id, department):
        """
        Initializes a Faculty object.
        Args:
            name (str): The name of the faculty member.
            age (int): The age of the faculty member.
            faculty_id (str): The unique ID for the faculty member.
            department (str): The department the faculty member belongs to.
        """
        super().__init__(name, age)
        self.faculty_id = faculty_id
        self.department = department
        self.courses_taught = []

    def assign_to_course(self, course_name):
        """Assigns the faculty member to teach a course."""
        if course_name not in self.courses_taught:
            self.courses_taught.append(course_name)
            print(f"{self.name} has been assigned to teach {course_name}.")
        else:
            print(f"{self.name} is already teaching {course_name}.")

    def get_details(self):
        """Returns detailed information about the faculty member."""
        # Calling the parent method and adding more details
        person_details = super().get_details()
        return f"{person_details}, Faculty ID: {self.faculty_id}, Department: {self.department}"

    def get_responsibilities(self):
        """Overrides the parent method to return faculty-specific responsibilities."""
        return "To teach courses, conduct research, and advise students."