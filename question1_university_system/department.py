class Course:
    def __init__(self, name, code, max_enrollment, prerequisites=None):
        self.name = name
        self.code = code
        self.max_enrollment = max_enrollment
        self.prerequisites = prerequisites or []
        self.enrolled_students = []
        self.faculty = None

    def enroll_student(self, student):
        if len(self.enrolled_students) < self.max_enrollment:
            if all(prereq in student.courses for prereq in self.prerequisites):
                self.enrolled_students.append(student)
                student.enroll_course(self.code)
                return True
        return False

    def assign_faculty(self, faculty):
        self.faculty = faculty


class Department:
    def __init__(self, name):
        self.name = name
        self.faculty = []
        self.courses = []
        self.students = []

    def add_faculty(self, faculty):
        self.faculty.append(faculty)

    def add_course(self, course):
        self.courses.append(course)

    def add_student(self, student):
        self.students.append(student)
