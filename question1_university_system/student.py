from person import Person

class Student(Person):
    """A class to represent a student, inheriting from Person."""

    def __init__(self, name, age, student_id, department):
        """
        Initializes a Student object.
        Args:
            name (str): The name of the student.
            age (int): The age of the student.
            student_id (str): The unique ID for the student.
            department (str): The department the student belongs to.
        """
        super().__init__(name, age)
        self.student_id = student_id
        self.department = department
        # Using a dictionary to store enrolled courses and their grades
        self.courses = {}

    def enroll_course(self, course_name, grade=None):
        """Enrolls the student in a course."""
        if course_name not in self.courses:
            self.courses[course_name] = grade
            print(f"{self.name} has enrolled in {course_name}.")
        else:
            print(f"{self.name} is already enrolled in {course_name}.")

    def drop_course(self, course_name):
        """Drops a course for the student."""
        if course_name in self.courses:
            del self.courses[course_name]
            print(f"{self.name} has dropped {course_name}.")
        else:
            print(f"{self.name} is not enrolled in {course_name}.")

    def calculate_gpa(self):
        """
        Calculates the GPA for the student.
        Assumes grades are on a 4.0 scale.
        """
        grades = [grade for grade in self.courses.values() if grade is not None]
        if not grades:
            return 0.0
        return sum(grades) / len(grades)

    def get_academic_status(self):
        """Determines the academic status of the student based on GPA."""
        gpa = self.calculate_gpa()
        if gpa >= 3.5:
            return "Dean's List"
        elif gpa >= 2.0:
            return "Good Standing"
        else:
            return "Probation"
        
    def get_details(self):
        """Returns detailed information about the student."""
        # Calling the parent method and adding more details
        person_details = super().get_details()
        return f"{person_details}, Student ID: {self.student_id}, Department: {self.department}"

    def get_responsibilities(self):
        """Overrides the parent method to return student-specific responsibilities."""
        return "To study, attend classes, and complete assignments."
        